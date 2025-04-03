package Teste1;

import java.io.*;
import java.net.*;
import java.util.zip.*;

class TESTE1_web_scraping{
    public static void main(String[] args) {
        // Definindo os links para os PDFs
        String url1 = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos/Anexo_I_Rol_2021RN_465.2021_RN627L.2024.pdf";
        String url2 = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos/Anexo_II_DUT_2021_RN_465.2021_RN628.2025_RN629.2025.pdf";

        // Caminhos locais onde os PDFs serão salvos
        String pdf1Path = "Teste1/Anexo_I.pdf";
        String pdf2Path = "Teste1/Anexo_II.pdf";

        try{
            //Baixando os pdfs
            downloadFile(url1, pdf1Path);
            downloadFile(url2, pdf2Path);

            //Compactando
            zipFiles("Teste1/Anexos.zip",pdf1Path,pdf2Path);
            System.out.println("Os arquivos foram baixados e compactados com sucesso!");

        }catch(IOException e){
            System.out.println("Ocorreu um erro: " + e.getMessage());
        }
    }

    private static void downloadFile(String fileURL, String savePath) throws IOException {
        //Criando a URL a partir do link
        URL url = new URL(fileURL);

        //abrindo a conexão http
        HttpURLConnection httpURLConnection = (HttpURLConnection) url.openConnection();
        int responseCode = httpURLConnection.getResponseCode(); //solicitacao bem sucessida ou não, 200,404

        if(responseCode == HttpURLConnection.HTTP_OK){
            //Abre os fluxos de leitura e escrita
            InputStream inputStream = httpURLConnection.getInputStream();
            FileOutputStream outputStream = new FileOutputStream(savePath);

            //buffer para armazenamento de dados temporarios
            byte[] buffer = new byte[4096];
            int bytesRead;

            //lê o arquivo e escreve no disco
            while((bytesRead = inputStream.read(buffer)) != -1){
                outputStream.write(buffer, 0 ,bytesRead); //escreve no arquivo de saida
            }

            //fechando os fluxos
            inputStream.close();
            outputStream.close();
        }else{
            throw new IOException("Não foi possivel baixar o arquivo. Código de resposta: ");
        }
    }

    //função para trasformar os arquivos em um unico zip
    public static void zipFiles(String zipFileName,String... filesToZip) throws IOException{ //usando varargs
        //Criacao do arquivo Zip
        FileOutputStream fos = new FileOutputStream(zipFileName);
        ZipOutputStream zipOut = new ZipOutputStream(fos);   //escreve os dados

        for(String filePath : filesToZip){
            File fileToZip = new File(filePath);
            FileInputStream fis = new FileInputStream(fileToZip); //le o conteudo do arquivo

            //Criacao de uma nova entrada no arquivo zip
            ZipEntry zipEntry = new ZipEntry(fileToZip.getName());
            zipOut.putNextEntry(zipEntry);

            //lê o arquivo e escreve no ZIP
            byte[] buffer = new byte[4096];
            int bytesRead;

            while((bytesRead = fis.read(buffer)) != -1){
                zipOut.write(buffer,0,bytesRead);
            }
            //Fecha a entrada do arquivo no ZIP e o arquivo de entrada
            zipOut.closeEntry();
            fis.close();
        }

        // Fechando o fluxo do ZIP
        zipOut.close();
        fos.close();

    }
}

