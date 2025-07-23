import qrcode
import requests
import io
import logging

logging.basicConfig(level=logging.INFO)

class QrCodeService:
    def __init__(self):
        """
        Initializes the QrCodeService class.
        This class is responsible for generating and uploading QR codes.
        """
        self.catbox_url = 'https://catbox.moe/user/api.php'
        
    def qr_code_generator(self, url_to_qr:str):
        """
        Gera QR code e faz upload para serviço online
        
        Args:
            url_to_qr (str): URL para gerar o QR code
        
        Returns:
            dict: Resultado do upload
        """
        # Validar URL
        if not url_to_qr.startswith(('http://', 'https://')):
            url_to_qr = 'https://' + url_to_qr
        
        # Gerar QR code
        img_bytes = self._generate_qr_code(url_to_qr)
        
        if not img_bytes:
            logging.error(f"Falha ao gerar QR code")
            return {'success': False, 'error': 'Falha ao gerar QR code'}
        
        # Fazer upload
        return self._upload_to_catbox(img_bytes)
    
    def _generate_qr_code(self, url: str, size:int=10, border:int=4, format:str='PNG'):
        """
        Gera um QR code em memória
        
        Args:
            url (str): URL para gerar o QR code
            tamanho (int): Tamanho do QR code
            borda (int): Tamanho da borda
            formato (str): Formato da imagem
        
        Returns:
            BytesIO: Imagem em bytes
        """
        try:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=size,
                border=border,
            )
            
            qr.add_data(url)
            qr.make(fit=True)
            
            img = qr.make_image(fill_color="black", back_color="white")
            
            # Salvar em BytesIO
            img_bytes = io.BytesIO()
            img.save(img_bytes, format=format)
            img_bytes.seek(0)
            
            return img_bytes
            
        except Exception as e:
            logging.error(f"Erro ao gerar QR Code: {str(e)}")
            return None
        
    def _upload_to_catbox(self, img_bytes):
        """Upload para Catbox.moe (gratuito, sem API key)"""
        try:
            img_bytes.seek(0)
            
            files = {'fileToUpload': ('qrcode.png', img_bytes, 'image/png')}
            data = {'reqtype': 'fileupload'}
            
            response = requests.post(self.catbox_url, files=files, data=data)
            
            if response.status_code == 200 and response.text.startswith('https://'):
                return {
                    'success': True,
                    'url': response.text.strip(),
                    'service': 'Catbox'
                }

            logging.error("Falha no upload para Catbox")
            return {'success': False, 'error': 'Falha no upload para Catbox'}
            
        except Exception as e:
            logging.error(f"Erro ao salvar no Catbox: {str(e)}")
            return {'success': False, 'error': f'Erro Catbox: {str(e)}'}