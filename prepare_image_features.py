"""Características do DINO (ViT-B/16 congelado) para o estudo com imagens.

Extrai uma única vez o vetor CLS (768 dimensões) de cada imagem e grava no
mesmo formato das bases tabulares, para que run_gcd.py e run_c4.py rodem sem
mudança, só em CPU:

    data_img/<base>/X_train.npy   características (float32, n x 768)
    data_img/<base>/y_train.npy   rótulos
    data_img/<base>/split.json    classes conhecidas e novas
    data_img/<base>/preproc.json  {"l2": true}: normaliza cada vetor (cosseno),
                                  como em Vaze et al.; desliga a padronização
    data_img/<base>/meta.json     origem, modelo, tamanho, divisão usada

Protocolo de Vaze et al. (GCD, CVPR 2022), o mesmo do SimGCD:
  - usa o conjunto de TREINO de cada base (transdutivo);
  - CIFAR-10: classes 0 a 4 conhecidas; CIFAR-100: classes 0 a 79 conhecidas;
  - CUB: divisão do SSB (Semantic Shift Benchmark). O arquivo da divisão vem
    do repositório do SimGCD (data/ssb_splits/cub_osr_splits.pkl); passe com
    --ssb-split. Sem ele, usa as 100 primeiras classes como conhecidas e
    registra isso no meta.json (NÃO comparável com os números publicados);
  - metade das amostras das classes conhecidas é rotulada: isso é feito
    depois, pelo run_gcd.py (--labeled-frac 0.5, por semente).
Pré-processamento das imagens: redimensiona para 256 (bicúbico), recorte
central de 224, normalização do ImageNet. Sem aumento de dados.

Precisa de internet (baixa as bases e os pesos do DINO) e de:
    pip install torch torchvision certifi timm
(timm só é usado se o download dos pesos pelo torch.hub falhar.)

Uso:
    python prepare_image_features.py --only cifar10 --max-samples 5000   # teste rápido
    python prepare_image_features.py --only cifar10 cifar100
    python prepare_image_features.py --only cub --ssb-split cub_osr_splits.pkl
"""
import argparse
import json
import os
import pickle
import time

import numpy as np

try:  # o Python do python.org no macOS não usa os certificados do sistema;
    import certifi  # o pacote certifi traz uma lista atualizada
    os.environ.setdefault("SSL_CERT_FILE", certifi.where())
except ImportError:
    pass

CUB_URL = "https://data.caltech.edu/records/65de6-vp158/files/CUB_200_2011.tgz"
BASES = ("cifar10", "cifar100", "cub")


def pick_device(name):
    import torch
    if name != "auto":
        return torch.device(name)
    if torch.cuda.is_available():
        return torch.device("cuda")
    if getattr(torch.backends, "mps", None) is not None and torch.backends.mps.is_available():
        return torch.device("mps")  # Mac com Apple Silicon
    return torch.device("cpu")


def load_dino(source):
    """DINO ViT-B/16; a saída é o vetor CLS (768).

    'hub': pesos oficiais via torch.hub (dl.fbaipublicfiles.com).
    'timm': os mesmos pesos, hospedados no Hugging Face (pip install timm).
    'auto': tenta o hub e, se o download falhar, usa o timm.
    """
    import torch
    if source in ("hub", "auto"):
        try:
            return torch.hub.load("facebookresearch/dino:main", "dino_vitb16"), "torch.hub facebookresearch/dino"
        except Exception as e:  # noqa: BLE001
            if source == "hub":
                raise
            print(f"AVISO: o download pelo torch.hub falhou ({type(e).__name__}: {e}).\n"
                  "       Tentando os mesmos pesos pelo timm (Hugging Face).")
    try:
        import timm
    except ImportError as e:
        raise SystemExit("Instale o timm para baixar os pesos pelo Hugging Face:\n"
                         "    pip install timm") from e
    return (timm.create_model("vit_base_patch16_224.dino", pretrained=True, num_classes=0),
            "timm vit_base_patch16_224.dino")


def build_transform():
    from torchvision import transforms
    from torchvision.transforms import InterpolationMode
    return transforms.Compose([
        transforms.Resize(256, interpolation=InterpolationMode.BICUBIC),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225)),
    ])


class CUBTrain:
    """Conjunto de treino do CUB-200-2011 (5.994 imagens), rótulos de 0 a 199."""

    def __init__(self, root, transform, download=True):
        from torchvision.datasets.utils import download_and_extract_archive
        self.base = os.path.join(root, "CUB_200_2011")
        if not os.path.isdir(self.base):
            if not download:
                raise FileNotFoundError(f"{self.base} não existe; baixe o CUB ou tire --no-download")
            download_and_extract_archive(CUB_URL, root, filename="CUB_200_2011.tgz")

        def read(name):
            with open(os.path.join(self.base, name)) as f:
                return dict(line.strip().split(" ", 1) for line in f if line.strip())

        paths, labels, is_train = read("images.txt"), read("image_class_labels.txt"), read("train_test_split.txt")
        ids = [i for i in paths if is_train[i] == "1"]
        self.files = [os.path.join(self.base, "images", paths[i]) for i in ids]
        self.targets = [int(labels[i]) - 1 for i in ids]
        self.transform = transform

    def __len__(self):
        return len(self.files)

    def __getitem__(self, i):
        from PIL import Image
        return self.transform(Image.open(self.files[i]).convert("RGB")), self.targets[i]


def load_base(name, root, transform, ssb_split, download):
    """Devolve (dataset, rótulos, classes conhecidas, descrição da divisão)."""
    from torchvision import datasets
    if name == "cifar10":
        ds = datasets.CIFAR10(root, train=True, download=download, transform=transform)
        return ds, np.asarray(ds.targets), list(range(5)), "Vaze et al.: classes 0-4 conhecidas"
    if name == "cifar100":
        ds = datasets.CIFAR100(root, train=True, download=download, transform=transform)
        return ds, np.asarray(ds.targets), list(range(80)), "Vaze et al.: classes 0-79 conhecidas"
    if name == "cub":
        ds = CUBTrain(root, transform, download)
        y = np.asarray(ds.targets)
        if ssb_split:
            with open(ssb_split, "rb") as f:
                info = pickle.load(f)
            known = sorted(int(c) for c in info["known_classes"])
            return ds, y, known, f"SSB ({os.path.basename(ssb_split)})"
        print("AVISO: sem --ssb-split; usando as 100 primeiras classes do CUB como "
              "conhecidas. Isso NÃO é a divisão do SimGCD.")
        return ds, y, list(range(100)), "100 primeiras classes (não é a divisão SSB do SimGCD)"
    raise ValueError(name)


def stratified_subset(y, max_samples, rng):
    """Índices de uma subamostra estratificada (mantém a proporção das classes)."""
    if not max_samples or len(y) <= max_samples:
        return np.arange(len(y))
    idx = []
    for c in np.unique(y):
        ic = np.flatnonzero(y == c)
        n = max(2, int(round(len(ic) * max_samples / len(y))))
        idx.append(rng.choice(ic, min(n, len(ic)), replace=False))
    return np.sort(np.concatenate(idx))


def extract(model, ds, idx, device, batch_size, workers):
    import torch
    from torch.utils.data import DataLoader, Subset
    loader = DataLoader(Subset(ds, idx.tolist()), batch_size=batch_size, shuffle=False,
                        num_workers=workers)
    feats, t0, done = [], time.time(), 0
    with torch.no_grad():
        for x, _ in loader:
            feats.append(model(x.to(device)).float().cpu().numpy())
            done += len(x)
            rate = done / max(time.time() - t0, 1e-9)
            print(f"\r  {done}/{len(idx)} imagens, {rate:.0f}/s, "
                  f"faltam {(len(idx) - done) / max(rate, 1e-9) / 60:.1f} min", end="", flush=True)
    print()
    return np.concatenate(feats).astype(np.float32)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--only", nargs="+", choices=BASES, default=["cifar10", "cifar100"])
    ap.add_argument("--out", default="data_img", help="pasta de saída")
    ap.add_argument("--root", default="raw_img", help="onde as imagens são baixadas")
    ap.add_argument("--ssb-split", default=None,
                    help="cub_osr_splits.pkl do repositório do SimGCD (só para o CUB)")
    ap.add_argument("--max-samples", type=int, default=0,
                    help="subamostra estratificada (0 = todas); útil para um teste rápido")
    ap.add_argument("--batch-size", type=int, default=64)
    ap.add_argument("--workers", type=int, default=2)
    ap.add_argument("--device", default="auto", help="auto, cpu, mps ou cuda")
    ap.add_argument("--model-source", choices=["auto", "hub", "timm"], default="auto",
                    help="de onde baixar os pesos do DINO (auto: hub, depois timm)")
    ap.add_argument("--no-download", action="store_true")
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args()

    import torch
    device = pick_device(args.device)
    print(f"dispositivo: {device}")
    model, model_src = load_dino(args.model_source)  # Caron et al., 2021
    model = model.to(device).eval()
    print(f"modelo: {model_src}")
    transform = build_transform()
    rng = np.random.default_rng(args.seed)

    for name in args.only:
        print(f"[{name}]")
        ds, y_all, known, how = load_base(name, args.root, transform, args.ssb_split,
                                          not args.no_download)
        idx = stratified_subset(y_all, args.max_samples, rng)
        X = extract(model, ds, idx, device, args.batch_size, args.workers)
        y = y_all[idx]
        classes = np.unique(y)
        novel = [int(c) for c in classes if c not in set(known)]
        known = [int(c) for c in classes if c in set(known)]
        d = os.path.join(args.out, name)
        os.makedirs(d, exist_ok=True)
        np.save(os.path.join(d, "X_train.npy"), X)
        np.save(os.path.join(d, "y_train.npy"), y)
        with open(os.path.join(d, "split.json"), "w") as f:
            json.dump({"known": known, "novel": novel}, f)
        with open(os.path.join(d, "preproc.json"), "w") as f:
            json.dump({"l2": True}, f)
        meta = {"source": name, "subset": "train", "model": f"DINO ViT-B/16, CLS ({model_src})",
                "n": int(len(y)), "d": int(X.shape[1]), "classes": int(len(classes)),
                "known": len(known), "novel": len(novel), "split": how,
                "max_samples": args.max_samples, "seed": args.seed,
                "transform": "Resize(256, bicubic) + CenterCrop(224) + Normalize(ImageNet)"}
        with open(os.path.join(d, "meta.json"), "w") as f:
            json.dump(meta, f, indent=1)
        print(f"  salvo em {d}: X {X.shape}, {len(known)} classes conhecidas, {len(novel)} novas")
        print(f"  divisão: {how}")


if __name__ == "__main__":
    main()
