# Seed-VC  
[![Hugging Face](https://img.shields.io/badge/🤗%20Hugging%20Face-Demo-blue)](https://huggingface.co/spaces/Plachta/Seed-VC)  [![arXiv](https://img.shields.io/badge/arXiv-2411.09943-<COLOR>.svg)](https://arxiv.org/abs/2411.09943)

*English | [简体中文](README-ZH.md) | [日本語](README-JA.md)*  

[real-time-demo.webm](https://github.com/user-attachments/assets/86325c5e-f7f6-4a04-8695-97275a5d046c)

Currently released model supports *zero-shot voice conversion* 🔊 , *zero-shot real-time voice conversion* 🗣️ and *zero-shot singing voice conversion* 🎶. Without any training, it is able to clone a voice given a reference speech of 1~30 seconds.  

We support further fine-tuning on custom data to increase performance on specific speaker/speakers, with extremely low data requirement **(minimum 1 utterance per speaker)** and extremely fast training speed **(minimum 100 steps, 2 min on T4)**!

**Real-time voice conversion** is support, with algorithm delay of ~300ms and device side delay of ~100ms, suitable for online meetings, gaming and live streaming.

To find a list of demos and comparisons with previous voice conversion models, please visit our [demo page](https://plachtaa.github.io/seed-vc/)🌐  and [Evaluaiton](EVAL.md)📊.

We are keeping on improving the model quality and adding more features.

## Evaluation📊
See [EVAL.md](EVAL.md) for objective evaluation results and comparisons with other baselines.
## Installation📥
Suggested python 3.10 on Windows or Linux.
```bash
pip install -r requirements.txt
```

## Usage🛠️
We have released 3 models for different purposes:

| Version | Name                                                                                                                                                                                                                       | Purpose                        | Sampling Rate | Content Encoder | Vocoder | Hidden Dim | N Layers | Params | Remarks                                                |
|---------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------|---------------|-----------------|---------|------------|----------|--------|--------------------------------------------------------|
| v1.0    | seed-uvit-tat-xlsr-tiny ([🤗](https://huggingface.co/Plachta/Seed-VC/blob/main/DiT_uvit_tat_xlsr_ema.pth)[📄](configs/presets/config_dit_mel_seed_uvit_xlsr_tiny.yml))                                                     | Voice Conversion (VC)          | 22050         | XLSR-large      | HIFT    | 384        | 9        | 25M    | suitable for real-time voice conversion                |
| v1.0    | seed-uvit-whisper-small-wavenet ([🤗](https://huggingface.co/Plachta/Seed-VC/blob/main/DiT_seed_v2_uvit_whisper_small_wavenet_bigvgan_pruned.pth)[📄](configs/presets/config_dit_mel_seed_uvit_whisper_small_wavenet.yml)) | Voice Conversion (VC)          | 22050         | Whisper-small   | BigVGAN | 512        | 13       | 98M    | suitable for offline voice conversion                  |
| v1.0    | seed-uvit-whisper-base ([🤗](https://huggingface.co/Plachta/Seed-VC/blob/main/DiT_seed_v2_uvit_whisper_base_f0_44k_bigvgan_pruned_ft_ema.pth)[📄](configs/presets/config_dit_mel_seed_uvit_whisper_base_f0_44k.yml))       | Singing Voice Conversion (SVC) | 44100         | Whisper-small   | BigVGAN | 768        | 17       | 200M   | strong zero-shot performance, singing voice conversion |

Checkpoints of the latest model release will be downloaded automatically when first run inference.  
If you are unable to access huggingface for network reason, try using mirror by adding `HF_ENDPOINT=https://hf-mirror.com` before every command.

Command line inference:
```bash
python inference.py --source <source-wav>
--target <referene-wav>
--output <output-dir>
--diffusion-steps 25 # recommended 30~50 for singingvoice conversion
--length-adjust 1.0
--inference-cfg-rate 0.7
--f0-condition False # set to True for singing voice conversion
--auto-f0-adjust False # set to True to auto adjust source pitch to target pitch level, normally not used in singing voice conversion
--semi-tone-shift 0 # pitch shift in semitones for singing voice conversion
--checkpoint <path-to-checkpoint>
--config <path-to-config>
 --fp16 True
```
where:
- `source` is the path to the speech file to convert to reference voice
- `target` is the path to the speech file as voice reference
- `output` is the path to the output directory
- `diffusion-steps` is the number of diffusion steps to use, default is 25, use 30-50 for best quality, use 4-10 for fastest inference
- `length-adjust` is the length adjustment factor, default is 1.0, set <1.0 for speed-up speech, >1.0 for slow-down speech
- `inference-cfg-rate` has subtle difference in the output, default is 0.7 
- `f0-condition` is the flag to condition the pitch of the output to the pitch of the source audio, default is False, set to True for singing voice conversion  
- `auto-f0-adjust` is the flag to auto adjust source pitch to target pitch level, default is False, normally not used in singing voice conversion
- `semi-tone-shift` is the pitch shift in semitones for singing voice conversion, default is 0  
- `checkpoint` is the path to the model checkpoint if you have trained or fine-tuned your own model, leave to blank to auto-download default model from huggingface.(`seed-uvit-whisper-small-wavenet` if `f0-condition` is `False` else `seed-uvit-whisper-base`)
- `config` is the path to the model config if you have trained or fine-tuned your own model, leave to blank to auto-download default config from huggingface  
- `fp16` is the flag to use float16 inference, default is True

Voice Conversion Web UI:
```bash
python app_vc.py --checkpoint <path-to-checkpoint> --config <path-to-config> --fp16 True
```
- `checkpoint` is the path to the model checkpoint if you have trained or fine-tuned your own model, leave to blank to auto-download default model from huggingface. (`seed-uvit-whisper-small-wavenet`)
- `config` is the path to the model config if you have trained or fine-tuned your own model, leave to blank to auto-download default config from huggingface  

Then open the browser and go to `http://localhost:7860/` to use the web interface.

Singing Voice Conversion Web UI:
```bash
python app_svc.py --checkpoint <path-to-checkpoint> --config <path-to-config> --fp16 True
```
- `checkpoint` is the path to the model checkpoint if you have trained or fine-tuned your own model, leave to blank to auto-download default model from huggingface. (`seed-uvit-whisper-base`)
- `config` is the path to the model config if you have trained or fine-tuned your own model, leave to blank to auto-download default config from huggingface  

Integrated Web UI:
```bash
python app.py
```
This will only load pretrained models for zero-shot inference. To use custom checkpoints, please run `app_vc.py` or `app_svc.py` as above.

Real-time voice conversion GUI:
```bash
python real-time-gui.py --checkpoint <path-to-checkpoint> --config <path-to-config>
```
- `checkpoint` is the path to the model checkpoint if you have trained or fine-tuned your own model, leave to blank to auto-download default model from huggingface. (`seed-uvit-tat-xlsr-tiny`)
- `config` is the path to the model config if you have trained or fine-tuned your own model, leave to blank to auto-download default config from huggingface  

IMPORTANT: It is strongly recommended to use a GPU for real-time voice conversion.  
Some performance testing has been done on a NVIDIA RTX 3060 Laptop GPU, results and recommended parameter settings are listed below:

| Model Configuration             | Diffusion Steps | Inference CFG Rate | Max Prompt Length | Block Time (s) | Crossfade Length (s) | Extra context (left) (s) | Extra context (right) (s) | Latency (ms) | Inference Time per Chunk (ms) |
|---------------------------------|-----------------|--------------------|-------------------|----------------|----------------------|--------------------------|---------------------------|--------------|-------------------------------| 
| seed-uvit-xlsr-tiny             | 10              | 0.7                | 3.0               | 0.18s          | 0.04s                | 2.5s                     | 0.02s                     | 430ms        | 150ms                         |

You can adjust the parameters in the GUI according to your own device performance, the voice conversion stream should work well as long as Inference Time is less than Block Time.  
Note that inference speed may drop if you are running other GPU intensive tasks (e.g. gaming, watching videos)  

You may wish to use [VB-CABLE](https://vb-audio.com/Cable/) to route audio from GUI output stream to a virtual microphone.  

*(GUI and audio chunking logic are modified from [RVC](https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI), thanks for their brilliant implementation!)*

## Training🏋️
Fine-tuning on custom data allow the model to clone someone's voice more accurately. It will largely improve speaker similarity on particular speakers, but may slightly increase WER.  
A Colab Tutorial is here for you to follow: [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1R1BJTqMsTXZzYAVx3j1BiemFXog9pbQG?usp=sharing)
1. Prepare your own dataset. It has to satisfy the following:
    - File structure does not matter
    - Each audio file should range from 1 to 30 seconds, otherwise will be ignored
    - All audio files should be in on of the following formats: `.wav` `.flac` `.mp3` `.m4a` `.opus` `.ogg`
    - Speaker label is not required, but make sure that each speaker has at least 1 utterance
    - Of course, the more data you have, the better the model will perform
    - Training data should be as clean as possible, BGM or noise is not desired
2. Choose a model configuration file from `configs/presets/` for fine-tuning, or create your own to train from scratch.
    - For fine-tuning, it should be one of the following:
        - `./configs/presets/config_dit_mel_seed_uvit_xlsr_tiny.yml` for real-time voice conversion
        - `./configs/presets/config_dit_mel_seed_uvit_whisper_small_wavenet.yml` for offline voice conversion
        - `./configs/presets/config_dit_mel_seed_uvit_whisper_base_f0_44k.yml` for singing voice conversion
3. Run the following command to start training:
```bash
python train.py 
--config <path-to-config> 
--dataset-dir <path-to-data>
--run-name <run-name>
--batch-size 2
--max-steps 1000
--max-epochs 1000
--save-every 500
--num-workers 0
```
where:
- `config` is the path to the model config, choose one of the above for fine-tuning or create your own for training from scratch
- `dataset-dir` is the path to the dataset directory, which should be a folder containing all the audio files
- `run-name` is the name of the run, which will be used to save the model checkpoints and logs
- `batch-size` is the batch size for training, choose depends on your GPU memory.
- `max-steps` is the maximum number of steps to train, choose depends on your dataset size and training time
- `max-epochs` is the maximum number of epochs to train, choose depends on your dataset size and training time
- `save-every` is the number of steps to save the model checkpoint
- `num-workers` is the number of workers for data loading, set to 0 for Windows    

4. If training accidentially stops, you can resume training by running the same command again, the training will continue from the last checkpoint. (Make sure `run-name` and `config` arguments are the same so that latest checkpoint can be found)

5. After training, you can use the trained model for inference by specifying the path to the checkpoint and config file.
    - They should be under `./runs/<run-name>/`, with the checkpoint named `ft_model.pth` and config file with the same name as the training config file.
    - You still have to specify a reference audio file of the speaker you'd like to use during inference, similar to zero-shot usage.

## TODO📝
- [x] Release code
- [x] Release pretrained models: [![Hugging Face](https://img.shields.io/badge/🤗%20Hugging%20Face-SeedVC-blue)](https://huggingface.co/Plachta/Seed-VC)
- [x] Huggingface space demo: [![Hugging Face](https://img.shields.io/badge/🤗%20Hugging%20Face-Space-blue)](https://huggingface.co/spaces/Plachta/Seed-VC)
- [x] HTML demo page: [Demo](https://plachtaa.github.io/seed-vc/)
- [x] Streaming inference
- [x] Reduce streaming inference latency
- [x] Demo video for real-time voice conversion
- [x] Singing voice conversion
- [x] Noise resiliency for source audio
- [ ] Potential architecture improvements
    - [x] U-ViT style skip connections
    - [x] Changed input to OpenAI Whisper
    - [x] Time as Token
- [x] Code for training on custom data
- [x] Few-shot/One-shot speaker fine-tuning
- [x] Changed to BigVGAN from NVIDIA for singing voice decoding
- [x] Whisper version model for singing voice conversion
- [x] Objective evaluation and comparison with RVC/SoVITS for singing voice conversion
- [x] Improve audio quality
- [ ] NSF vocoder for better singing voice conversion
- [x] Fix real-time voice conversion artifact while not talking (done by adding a VAD model)
- [x] Colab Notebook for fine-tuning example
- [ ] More to be added

## CHANGELOGS🗒️
- 2024-11-26:
    - Updated v1.0 tiny version pretrained model, optimized for real-time voice conversion
    - Support one-shot/few-shot single/multi speaker fine-tuning
    - Support using custom checkpoint for webUI & real-time GUI
- 2024-11-19:
    - arXiv paper released
- 2024-10-28:
    - Updated fine-tuned 44k singing voice conversion model with better audio quality
- 2024-10-27:
    - Added real-time voice conversion GUI
- 2024-10-25:
    - Added exhaustive evaluation results and comparisons with RVCv2 for singing voice conversion
- 2024-10-24:
    - Updated 44kHz singing voice conversion model, with OpenAI Whisper as speech content input
- 2024-10-07:
    - Updated v0.3 pretrained model, changed speech content encoder to OpenAI Whisper
    - Added objective evaluation results for v0.3 pretrained model
- 2024-09-22:
    - Updated singing voice conversion model to use BigVGAN from NVIDIA, providing large improvement to high-pitched singing voices
    - Support chunking and  streaming output for long audio files in Web UI
- 2024-09-18:
    - Updated f0 conditioned model for singing voice conversion
- 2024-09-14:
    - Updated v0.2 pretrained model, with smaller size and less diffusion steps to achieve same quality, and additional ability to control prosody preservation
    - Added command line inference script
    - Added installation and usage instructions