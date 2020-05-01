Instruções para utilização do Private Feed na Azure

1- Efetue o download do client "nuget.exe" 4.8.0.5385 ou superior 
https://www.nuget.org/downloads

Caso esteja no Windows, basta colocar seu caminho de acesso nas variáveis de ambiente (no PATH). Caso Não esteja, deve ser seguido as instruções disponíveis no link a seguir

https://docs.microsoft.com/pt-br/nuget/reference/nuget-exe-cli-reference

https://dotnet.microsoft.com/download
2- Efetue o download do dotnet SDK 2.1.400 ou superior e instale-o

Caso esteja no Windows e não tenha o Visual Studio

- Instale o MsBuild atualizado
https://visualstudio.microsoft.com/pt-br/downloads/ (expandir grupo "Ferramentas para Visual Studio 2019" > "Ferramentas de Build para Visual Studio 2019")

- Execute o arquivo "installcredprovider.ps1", disponível neste mesmo diretório do GitHub, seguindo as instruções:
> Abra o PowerShell no modo Administrador
> execute o comando: Set-ExecutionPolicy Unrestricted -Scope CurrentUser -Force
> execute o comando: installcredprovider.ps1 

Caso não esteja no Windows, seguir as instruções do topico "Installation on Linux and Mac"
https://github.com/microsoft/artifacts-credprovider#azure-artifacts-credential-provider

3- Execute no console para efetuar as seguintes ações:

- Configurar o private feed
nuget.exe sources Add -Name "AzureMcarPrivateFeed" -Source "https://pkgs.dev.azure.com/arquitetura0301/CICDProject/_packaging/AzureMcarPrivateFeed/nuget/v3/index.json" -username unused -password "kcatxn4dr5dbtiy3nwblkreljqjfx3fn76lwb4hbwwmqeyytlnra"

Outra forma de adicionar um novo feed é criar um arquivo "nuget.config" por projeto, contendo as informações de conexão

<?xml version="1.0" encoding="utf-8"?>
<configuration>
  <packageSources>
    <clear />
	<add key="AzureMcarPrivateFeed" value="https://pkgs.dev.azure.com/arquitetura0301/CICDProject/_packaging/AzureMcarPrivateFeed/nuget/v3/index.json" />
  </packageSources>
  <packageSourceCredentials>
    <AzureMcarPrivateFeed>
        <add key="Username" value="unused" />
        <add key="Password" value="AQAAANCMnd8BFdERjHoAwE/Cl+sBAAAARo3l4osGhEaACTnhy7+1cQAAAAACAAAAAAADZgAAwAAAABAAAAAlGCQFV31a4rPlHtomQGKFAAAAAASAAACgAAAAEAAAANqKqZxq6x8hzzqY7aGnbc44AAAAXwSuYE/tYa35QD4RKYrR0aPaCezPptCTwuejBjYiJv5oBqKpXJQPPn9qo82n66zPnHiMTfZ2i7IUAAAA/3xSf17B7Dj4v9J89YKcfc+PdCE=" />
      </AzureMcarPrivateFeed>
  </packageSourceCredentials>  
</configuration>

ATENÇÃO: o Token utilizado no nuget.config é criptografado, então, caso seja alterado o Token utilizado no "AzureMcarPrivateFeed" (gh54ka6r4huygggkmd3xhumeiqaztqd4urwrv3cmvox7uny4jfsa), terá de ser usado a opção anterior (nuget.exe sources Add) usando o novo token.

- Lista feeds (sources) disponíveis, que ficam configurados no NuGet.config do %AppData%
nuget sources

- Publicar pacotes
nuget.exe push -Source "AzureMcarPrivateFeed" -ApiKey key <ARQUIVO>.nupkg

- Listar pacotes de private feeds
nuget list -source "https://pkgs.dev.azure.com/arquitetura0301/CICDProject/_packaging/AzureMcarPrivateFeed/nuget/v3/index.json"
nuget list -source "AzureMcarPrivateFeed"
nuget list -source "AzureMcarPrivateFeed" -AllVersions

- Remover pacote 
nuget delete <PACOTE> <VERSAO_PACOTE> -ApiKey key -source "AzureMcarPrivateFeed"

ATENÇÃO: Remover pacotes do Private Feed da Azure apenas torna indisponível o download do mesmo, mas aquele número de versão (X.X.X) continua reservado para aquele pacote, não sendo permitido subir outro pacote de mesmo nome e número de versão. Isso é uma restrição da Azure (sendo possível e comum de ser feito em outros provedores de Feeds).

- Adicionar pacote no projeto
Adicionar manualmente no arquivo csproj

  <ItemGroup>
    <PackageReference Include="MCar.Framework.Etc" Version="1.0.0" />
  </ItemGroup>

ou via console

dotnet add <NOME_PROJETO>.csproj package <NOME_PACOTE> -v <VERSAO_PACOTE>

- Restaurar versão do pacote


> Informações Adicionais

- Para configurar um novo Private Feed na Azure
Criar Token "AzurePrivateFeedCredential", e obter uma chave (a atual é "gh54ka6r4huygggkmd3xhumeiqaztqd4urwrv3cmvox7uny4jfsa")

Criar um novo Feed com as opções default (exceto a de permissão, que deve ser marcada a para utilizar os membros de sua organização), depois clicar no Feed > Connect to feed, e obter o valor da "Package source URL".

> How to solve artifact push errors:
  When error is like: "Unable to load the service index for source https://pkgs.dev.azure..." and "InvalidKey"
    Reason: You are using the old account (arquitetura@...) token key.
    Solution:
      1. Go to Devops, click upper-right "User Settings" then "Personal Access Tokens".
      2. Create your key and store it.
      3. Now you need to remove your local artifacts source that is using the old token:
        - nuget sources Remove -Name "AzureMcarPrivateFeed"
      4. Now create the token again:"
        - nuget.exe sources Add -Name "AzureMcarPrivateFeed" -Source "https://pkgs.dev.azure.com/arquitetura0301/CICDProject/_packaging/AzureMcarPrivateFeed/nuget/v3/index.json" -username unused -password "YOUR_KEY_HERE"
      5. Now you are authorized and can push your packages.

> Links de Referência

- Acesso ao site Dev da Azure
https://dev.azure.com/arquitetura0301/CICDProject/_packaging?_a=feed&feed=arquitetura0301

- Configurar o feed via IDE do Visual Studio
https://docs.microsoft.com/en-us/azure/devops/artifacts/nuget/consume?view=azure-devops

- Configurar provedores de credenciais no ambiente
https://github.com/microsoft/artifacts-credprovider#setup

- Configuração manual do arquivo nuget.config
https://docs.microsoft.com/en-us/nuget/reference/nuget-config-file

- Tutorial para utilizar o Feed da Azure
http://www.leerichardson.com/2019/04/share-code-like-boss-part-1-private.html