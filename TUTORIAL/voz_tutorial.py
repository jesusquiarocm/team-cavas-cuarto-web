import json, re, sys, warnings
from pathlib import Path
warnings.filterwarnings("ignore")
import torch, torchaudio
sys.path.insert(0, "/Users/jesusquiaro/Downloads/EDICIONES TCC/tools")
from voz_local import trozos
from chatterbox.mtl_tts import ChatterboxMultilingualTTS
R = Path("/Users/jesusquiaro/Downloads/EDICIONES TCC/referencias/voz/gemini_charon.wav")
dev = "mps" if torch.backends.mps.is_available() else "cpu"
m = ChatterboxMultilingualTTS.from_pretrained(device=dev)
sil = torch.zeros(1, int(m.sr*0.25))
out = Path(__file__).parent/"audio"
for e in json.loads((Path(__file__).parent/"guion.json").read_text()):
    partes=[]
    for t in trozos(e["texto"], 200):
        w = m.generate(t, language_id="es", audio_prompt_path=str(R), exaggeration=0.55, cfg_weight=0.3)
        partes += [w.cpu(), sil]
    a = torch.cat(partes[:-1], dim=1)
    torchaudio.save(str(out/f"{e['id']}.wav"), a, m.sr)
    print(e["id"], round(a.shape[1]/m.sr,1), flush=True)
