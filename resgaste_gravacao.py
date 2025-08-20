import paramiko
from paramiko import SSHClient
import os

class SftpUploader:
    def __init__(self):
        # Configurações do servidor SFTP
        self.HOST = " "
        self.PORT = " "
        self.USERNAME = " "   
        self.PASSWORD = " "   
        self.KEY_FILE = " "          

        # Diretórios
        #Diretório local 
        self.LOCAL_FILES_DIR = " "
        #Diretório remoto
        self.REMOTE_DIR = ""

     
    def op_sftp(self):
         
        ssh_client = None
        try:
            # Cria a pasta local (caso não exista)
            os.makedirs(self.LOCAL_FILES_DIR, exist_ok=True)
            
            # Cria o cliente SSH
            ssh_client = SSHClient()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            print(f"INFO: Carregando a chave privada...")
            private_key = paramiko.RSAKey.from_private_key_file(self.KEY_FILE)
            
            print(f"INFO: Conectando a {self.HOST}:{self.PORT}...")
            ssh_client.connect(
                hostname=self.HOST,
                port=self.PORT,
                username=self.USERNAME,
                password=self.PASSWORD,
                pkey=private_key,
                look_for_keys=False,
                timeout=15
            )
            
            print("Conexão estabelecida com sucesso!")
            
            with ssh_client.open_sftp() as sftp:
                print(f"INFO: Acessando o diretório remoto '{self.REMOTE_DIR}'...")
                sftp.chdir(self.REMOTE_DIR)
                
                # Verifica se tem permissão de escrita
                try:
                    sftp.stat('.')
                    print("Tem permissão de escrita no diretório")
                except:
                    print("ERRO: Sem permissão de escrita!")
                    return

                # Lista arquivos locais
                if os.path.isfile(self.LOCAL_FILES_DIR):
                    arquivos = [os.path.basename(self.LOCAL_FILES_DIR)]
                    local_dir = os.path.dirname(self.LOCAL_FILES_DIR)
                else:
                    arquivos = os.listdir(self.LOCAL_FILES_DIR)
                    local_dir = self.LOCAL_FILES_DIR

                if not arquivos:
                    print("Nenhum arquivo encontrado na pasta local.")
                else:
                    for arquivo in arquivos:
                        caminho_local = os.path.join(local_dir, arquivo)
                        
                        if os.path.isfile(caminho_local):
                            try:
                                print(f"Enviando: {arquivo}...")
                                
                                # CORREÇÃO: Use apenas o nome do arquivo
                                sftp.put(caminho_local, arquivo)
                                
                                # Confirmação
                                sftp.stat(arquivo)
                                print(f"Arquivo {arquivo} enviado com sucesso!")
                                
                                #Remove do Diretorio local
                                os.remove(caminho_local)
                                print(f"Arquivo {arquivo} removido da pasta local.")

                            
                            except Exception as e:
                                print(f"Erro ao enviar {arquivo}: {e}")
                                
        finally:
            if ssh_client:
                ssh_client.close()
                print("Conexão fechada.")

if __name__ == "__main__":
    sftp_manager = SftpUploader()
    sftp_manager.op_sftp()
    print("Operação SFTP concluída.")