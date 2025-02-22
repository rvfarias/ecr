import boto3
import csv

#Classe de repos
class Repo:
    def __init__(self, nome, creatData, lifecycle, storage, lastImage, lastRecordedPullTime):
        self.nome = nome
        self.creatData = creatData
        self.lifecycle = lifecycle
        self.storage = storage
        self.lastImage = lastImage
        self.lastRecordedPullTime = lastRecordedPullTime

session = boto3.Session(profile_name="RPE-NEWPROD", region_name="us-east-1")
ecr = session.client("ecr")

def get_repos_about_lifecycle_policy(response):
    list_repo = []
    qtd_repos = 0
    
    for repo in response["repositories"]:
        store = 0
        repo_name = repo["repositoryName"]
        created_at = repo["createdAt"]

        try:
            lifecycle_policy = ecr.get_lifecycle_policy(repositoryName=repo["repositoryName"])
            life = True
        
        except ecr.exceptions.LifecyclePolicyNotFoundException:
            life = False

        qtd_repos += 1

        images = ecr.list_images(repositoryName=repo_name)
        
        if not images["imageIds"]:  # Se não houver imagens, define valores padrão
            last_image_tag = "<Sem tag>"
            last_image_date = None
        else:
            # Obter detalhes das imagens
            image_details = ecr.describe_images(
                repositoryName=repo_name,
                imageIds=images["imageIds"]
            )["imageDetails"]
            #print(image_details)
            
            for img in image_details:
                store += img["imageSizeInBytes"]
            
            store = round(store/ (1024 ** 3), 2)
            print("repo: ", qtd_repos, " size: " , store)
            # Ordenar imagens pela data de envio 
            latest_image = max(image_details, key=lambda img: img["imagePushedAt"])
            
            #Pegando a imagem criada mais recentemente 
            last_image_tag = latest_image.get("imageTags", ["<Sem tag>"])[0]
            last_image_date = latest_image["imagePushedAt"]

            valid_images = [img for img in image_details if "lastRecordedPullTime" in img]

            if valid_images:  # Garante que a lista não esteja vazia antes de chamar max()
                # Ordenar imagens pela data de pull
                latest_pull = max(valid_images, key=lambda img: img["lastRecordedPullTime"])
                
                #Pegando a imagem utilizada recentemente           
                latest_pull_tag = latest_pull.get("imageTags", ["<Sem tag>"])[0]
                latest_pull_date = latest_pull["lastRecordedPullTime"]
            
            else:
                latest_pull_tag = None  # Caso nenhuma imagem tenha a chave
    
            #Verificando qual tem a data mais recente e adicionando no array
            if latest_pull_date < last_image_date:
                repo_obj = Repo(repo_name, created_at, life, store, last_image_tag, last_image_date)
                list_repo.append(repo_obj)                
            
            else:
                repo_obj = Repo(repo_name, created_at, life, store, latest_pull_tag, latest_pull_date)
                list_repo.append(repo_obj)
        
    return list_repo, qtd_repos



# Valida repositórios no geral
response = ecr.describe_repositories(maxResults=411)

list_repo, qtd_repos = get_repos_about_lifecycle_policy(response)
#print(list_repo)

with open('teste.csv', 'w') as csvfile:
    writer = csv.writer(csvfile, delimiter= ',')
    writer.writerow(['repositoryName', 'creatData', 'lifecycle', 'SIZE', 'lastImage', 'lastRecordedPullTime'])
    for arq2 in list_repo:
        str1 = str(arq2.storage) + 'GB'
        writer.writerow([arq2.nome, arq2.creatData, arq2.lifecycle, str1, arq2.lastImage, arq2.lastRecordedPullTime])

print("\nQuantidade de repositórios: ", qtd_repos)
