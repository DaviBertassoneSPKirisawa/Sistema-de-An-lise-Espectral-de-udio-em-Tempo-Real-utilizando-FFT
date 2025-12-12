# 📡 Sistema de Análise Espectral de Áudio em Tempo Real

Projeto desenvolvido para a disciplina de **Processamento Digital de Sinais (PDS)**.  
O sistema captura áudio do microfone, aplica janelação, calcula a FFT (Transformada Rápida de Fourier) e exibe o espectro de frequências **em tempo real**.

---

## 🎯 Objetivo do Projeto

Criar um sistema capaz de:

- Capturar áudio em tempo real pelo microfone.
- Segmentar o sinal em blocos.
- Aplicar uma janela (Hann) para reduzir distorções.
- Calcular o espectro de frequências usando a FFT.
- Exibir uma visualização gráfica atualizada várias vezes por segundo.
- Mostrar a frequência dominante do sinal.

Nenhum hardware externo é necessário além de um microfone comum.

---

## 🧪 Tecnologias Utilizadas

- **Python 3.8+**
- `sounddevice` — captura de áudio em tempo real
- `numpy` — operações numéricas
- `scipy.signal` — janelas de sinal
- `matplotlib` — visualização do espectro
- `queue` — gerenciamento de áudio em tempo real

---

## 📁 Estrutura do Projeto

/
├── app.py # Código principal do analisador espectral
├── README.md # Instruções do projeto
├── requirements.txt # Dependências (opcional, mas recomendado)
└── screenshots/ # Imagens utilizadas no relatório


---

## ⚙️ Instalação e Execução

### Verificar ID do microfone
```powershell
python -c "import sounddevice as sd; print(sd.query_devices())"

O ID que deve ser escolhido é cumpre os melhores requisitos (WASAPI (2 in, 0 out))
"in" deve ser maior que 0
```
### 1️⃣ Criar ambiente virtual

```powershell
python -m venv venv

2️⃣ Ativar o ambiente virtual (Windows)
.\venv\Scripts\Activate.ps1

3️⃣ Instalar dependências
pip install sounddevice numpy scipy matplotlib

4️⃣ Executar o sistema
python app.py

A interface do espectro deve abrir imediatamente.
Fale, bata palma ou toque um som para observar o gráfico reagir em tempo real.

🔧 Parâmetros configuráveis (em app.py)
SR = 48000            # taxa de amostragem
BLOCK_DURATION = 0.05 # duração de cada bloco (latência)
FFT_SIZE = 4096       # tamanho da FFT
DEVICE = 12           # ID do microfone (defina com sd.query_devices())
WINDOW = 'hann'       # tipo de janela
SMOOTHING = 0.6       # suavização do espectro


Como ajustar:

SR: 44100 ou 48000
BLOCK_DURATION: menor → menor atraso / maior consumo de CPU
FFT_SIZE: maior → melhor resolução de frequência
DEVICE: execute:
python -c "import sounddevice as sd; print(sd.query_devices())"

WINDOW: hann recomendado
SMOOTHING: valores entre 0 e 0.99


🖼️ Evidências (Screenshots)
screenshots/
Insira imagens contendo:

Espectro de tom grave
Espectro de tom agudo
Frequência dominante exibida
Testes com ruído/voz
Essas imagens serão usadas no relatório.


🛠️ Problemas Comuns

❌ Error opening InputStream: Invalid sample rate
Seu microfone não suporta a taxa configurada.
→ Troque SR para 44100 ou 48000.

❌ No module named 'sounddevice'
Dependência instalada fora do venv.
→ Ative o venv novamente e reinstale.

❌ Gráfico em branco
Verifique:
Se o DEVICE é o ID correto
Se o microfone está ativo
Se há permissões de áudio


📜 Licença
Projeto desenvolvido exclusivamente para fins acadêmicos, como parte da disciplina de PDS.
