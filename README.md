📡 Sistema de Análise Espectral de Áudio em Tempo Real

Projeto desenvolvido para a disciplina de Processamento Digital de Sinais (PDS).
O sistema captura áudio do microfone, aplica janelação, calcula a FFT (Transformada Rápida de Fourier) e exibe o espectro de frequências em tempo real.

🎯 Objetivo do Projeto

Criar um sistema capaz de:

Capturar áudio em tempo real pelo microfone.

Segmentar o sinal em blocos.

Aplicar uma janela (Hann) para reduzir distorções.

Calcular o espectro de frequências usando a FFT.

Exibir uma visualização gráfica atualizada várias vezes por segundo.

Mostrar a frequência dominante do sinal.

Nenhum hardware externo é necessário além de um microfone comum.

🧪 Tecnologias Utilizadas

Python 3.8+

sounddevice — captura de áudio em tempo real

numpy — operações numéricas

scipy.signal — janelas de sinal

matplotlib — visualização do espectro

queue — gerenciamento de fluxo de dados em tempo real

📁 Estrutura do Projeto
/
├── app.py               # Código principal do analisador espectral
├── README.md            # Instruções do projeto
├── requirements.txt     # Dependências (opcional, mas recomendado)
└── screenshots/         # Imagens utilizadas no relatório (opcional)

⚙️ Instalação e Execução
1️⃣ Criar ambiente virtual
python -m venv venv

2️⃣ Ativar o ambiente virtual

Windows (PowerShell):

.\venv\Scripts\Activate.ps1


Você deve ver isso no terminal:

(venv) C:\caminho\do\projeto>

3️⃣ Instalar dependências
pip install sounddevice numpy scipy matplotlib

4️⃣ Executar o sistema
python app.py


A interface do espectro deve abrir imediatamente.
Fale, bata palma ou toque um som para observar o comportamento do gráfico.

🔧 Parâmetros configuráveis (em app.py)

No topo do arquivo você encontra:

SR = 48000            # taxa de amostragem
BLOCK_DURATION = 0.05 # duração de cada bloco (latência)
FFT_SIZE = 4096       # tamanho da FFT
DEVICE = 12           # ID do microfone (defina com sd.query_devices())
WINDOW = 'hann'       # tipo de janela
SMOOTHING = 0.6       # suavização do espectro

Como ajustar:

SR: 44100 ou 48000

BLOCK_DURATION: menor → menos atraso, mais carga de CPU

FFT_SIZE: maior → melhor resolução de frequência

DEVICE: use

python -c "import sounddevice as sd; print(sd.query_devices())"


e escolha o ID correto

WINDOW: geralmente 'hann'

SMOOTHING: entre 0 e 0.99

🖼️ Evidências

Screenshots do espectro podem ser inseridas na pasta screenshots/
e usadas no relatório, como:

Tom grave

Tom agudo

Palma

Ruído ambiente

🛠️ Problemas Comuns
❌ Error opening InputStream: Invalid sample rate

Seu microfone não suporta a taxa definida.
→ Altere SR para 44100 ou 48000.

❌ No module named 'sounddevice'

Você instalou a dependência fora do venv.
→ Ative o venv e reinstale.

❌ Nothing shows on the graph

Verifique:

DEVICE correto

microfone funcionando

volume/ganho

📜 Licença

Projeto desenvolvido exclusivamente para fins acadêmicos.

Se quiser, posso gerar também um requirements.txt, ou te ajudar a montar o README completo com GIF animado, ou até um vídeo de demonstração. Só pedir!
