# Servidor de Páginas HTTP

O código a seguir implementa um servidor de páginas HTTP que lista os arquivos de um diretório específico e permite o download dos arquivos solicitados. Além disso, possui um caminho especial "/HEADER" para retornar o cabeçalho HTTP da requisição.

## Como executar o servidor
  1. Abra um terminal ou prompt de comando.
  2. Navegue até o diretório onde o arquivo meu_servidor.py está localizado.
  3. Execute o seguinte comando:
  ```
    bash
    Copy code
    python3 meu_servidor.py
  ```
  4. O servidor começará a escutar na porta 8000 por padrão. Você pode alterar a porta editando a variável port no código, se desejar.
  5.   Acesse o servidor em seu navegador usando o seguinte URL: http://localhost:8000.

## Estrutura de diretórios
O diretório raiz do servidor deve conter os arquivos que serão listados e disponíveis para download.
Você pode ajustar o diretório raiz editando a variável directory no código.

## Funcionalidades
Ao acessar o servidor pelo navegador, você verá uma lista dos arquivos e pastas no diretório raiz.
Os arquivos serão exibidos com seus respectivos nomes, e você pode clicar nos links para visualizá-los ou fazer o download.
As pastas serão exibidas com seus respectivos nomes, e você pode clicar nos links para acessar seu conteúdo.
O caminho especial "/HEADER" retorna o cabeçalho HTTP da requisição feita.

## Observações
Certifique-se de que a porta utilizada pelo servidor esteja aberta e não esteja sendo usada por outros serviços em seu sistema.
Verifique se os arquivos e pastas no diretório raiz têm as permissões adequadas para serem lidos e acessados pelo servidor.