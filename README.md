# Sistema de Análise Espectral de Áudio em Tempo Real
Projeto desenvolvido para a disciplina de Processamento Digital de Sinais (PDS).  
O sistema captura áudio do microfone em tempo real, aplica janelação e calcula a Transformada Rápida de Fourier (FFT), exibindo o espectro de frequências em uma interface gráfica.

---

## 🎯 Objetivo do Projeto
Implementar um sistema em **tempo real** que:
- Captura áudio do microfone.
- Segmenta o sinal em blocos.
- Aplica janela (Hann).
- Calcula a FFT continuamente.
- Exibe o espectro de frequência atualizado.
- Mostra a frequência dominante do sinal.

Nenhum hardware adicional é necessário além de um microfone comum.

---

## 🧩 Tecnologias Utilizadas
- **Python 3.8+**
- `sounddevice` — captura de áudio em tempo real  
- `numpy` — processamento numérico  
- `scipy.signal` — janelas (Hann, Hamming etc.)  
- `matplotlib` — exibição gráfica do espectro  

---

## 📁 Estrutura do Projeto
/
├── app.py # código principal do sistema
├── README.md # este arquivo
├── requirements.txt # dependências (opcional)
└── screenshots/ # imagens usadas no relatório

## 🔧 Onde alterar os parâmetros
SR = 48000              # taxa de amostragem (Hz)
BLOCK_DURATION = 0.05   # duração de cada bloco (segundos)
CHANNELS = 1            # mono
DEVICE = 12             # ID do microfone (obtido via sd.query_devices())
WINDOW = 'hann'         # tipo de janela
SMOOTHING = 0.6         # suavização temporal entre frames
DEFAULT_FFT = 4096      # FFT mínima recomendada
