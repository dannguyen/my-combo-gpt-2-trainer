#!/usr/bin/env python

# import gpt_2_simple as gpt2
from pathlib import Path
import requests
from sys import stderr, stdout
from tqdm import tqdm, trange
from urllib.parse import urljoin

CHECKPOINTS_DIR = 'data/models/checkpoints'
DEFAULT_MODEL = '124M'
DOWNLOAD_CHUNK_SIZE = 1024 * 1024
MODELS_DIR = Path('data', 'models')
MODELS_SRCDOMAIN = 'https://storage.googleapis.com'
MODEL_COMPONENT_FILENAMES = ['checkpoint', 'encoder.json', 'hparams.json',
                      'model.ckpt.data-00000-of-00001', 'model.ckpt.index',
                      'model.ckpt.meta', 'vocab.bpe']

def get_model_subdir(model_name):
    return Path(MODELS_DIR).joinpath(model_name)


def get_model_files(model_name):
    mdir = get_model_subdir(model_name)
    return = [mdir.joinpath(bname) for bname in MODEL_COMPONENT_FILENAMES]

def fetch_model(model_name):
    """
    adapted from: gpt2.download_file_with_progress

    Downloads model files if needed
    """
    model_subdir = get_model_subdir(model_name)
    model_subdir.mkdir(exist_ok=True, parents=True)
    model_paths = get_model_files(model_name)

    if not all(p.exists() for p in model_paths):
        for destpath in model_paths:
            if not destpath.exists():
                srcurl = urljoin(MODELS_SRCDOMAIN, f"gpt-2/models/{model_name}/{destpath.name}")
                stderr.write(f"For model {model_name}, downloading: {srcurl}\n\twritng to: {destpath}\n")

                r = requests.get(srcurl, stream=True)
                with open(destpath, 'wb') as f:
                    file_size = int(r.headers["content-length"])
                    with tqdm(ncols=100, desc=f"Fetching {destpath}", total=file_size, unit_scale=True) as pbar:

                        for chunk in r.iter_content(chunk_size=DOWNLOAD_CHUNK_SIZE):
                            f.write(chunk)
                            pbar.update(DOWNLOAD_CHUNK_SIZE)



def fine_tune(session, src_path, model_path, checkpoint_dir=CHECKPOINTS_DIR, steps=1000):
    """
gpt2.finetune(sess,
              file_name,
              model_name=model_name,
              steps=1000)   # steps is max number of training steps

    adapted from: gpt2.finetune()
    https://github.com/minimaxir/gpt-2-simple/blob/master/gpt_2_simple/gpt_2.py#L127

    assumes model files have already been downloaded
    """
    checkpoint_dir.mkdir(exist_ok=True, parents=True)



def train(model):
    import gpt_2_simple as gpt2
    sesh = gpt2.start_tf_sess()


def main():
    fetch_model(DEFAULT_MODEL)
#    sesh = gpt2.start_tf_sess()



if __name__ == '__main__':
    main()
