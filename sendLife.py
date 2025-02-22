import boto3
import json

session = boto3.Session(profile_name="", region_name="us-east-1")
ecr = session.client("ecr")

def get_repos(response):
    qtd_repos = 0
    for repo in response["repositories"]:
    
        repo_name = repo["repositoryName"]

        lifecycle_policy= {
  "rules": [
    {
      "rulePriority": 1,
      "description": "Remove imagens com a tag SNAPSHOT",
      "selection": {
        "tagStatus": "tagged",
        "tagPrefixList": [
          "SNAPSHOT"
        ],
        "countType": "imageCountMoreThan",
        "countNumber": 5
      },
      "action": {
        "type": "expire"
      }
    },
    {
      "rulePriority": 2,
      "description": "Remove imagens com a tag RELEASE",
      "selection": {
        "tagStatus": "tagged",
        "tagPrefixList": [
          "RELEASE"
        ],
        "countType": "imageCountMoreThan",
        "countNumber": 5
      },
      "action": {
        "type": "expire"
      }
    },
    {
      "rulePriority": 3,
      "description": "Remove imagens SEM TAG",
      "selection": {
        "tagStatus": "untagged",
        "countType": "sinceImagePushed",
        "countUnit": "days",
        "countNumber": 1
      },
      "action": {
        "type": "expire"
      }
    },
    {
      "rulePriority": 4,
      "description": "Remove imagens com a tag TESTE",
      "selection": {
        "tagStatus": "tagged",
        "tagPrefixList": [
          "TESTE"
        ],
        "countType": "imageCountMoreThan",
        "countNumber": 7
      },
      "action": {
        "type": "expire"
      }
    },
    {
      "rulePriority": 5,
      "description": "Remove imagens com TAG qa-1 > 10",
      "selection": {
        "tagStatus": "tagged",
        "tagPrefixList": [
          "QA-1"
        ],
        "countType": "imageCountMoreThan",
        "countNumber": 7
      },
      "action": {
        "type": "expire"
      }
    },
    {
      "rulePriority": 6,
      "description": "Remove imagens com TAG qa-2 > 10",
      "selection": {
        "tagStatus": "tagged",
        "tagPrefixList": [
          "QA-2"
        ],
        "countType": "imageCountMoreThan",
        "countNumber": 7
      },
      "action": {
        "type": "expire"
      }
    },
    {
      "rulePriority": 7,
      "description": "Remove imagens com TAG qa-3 > 10",
      "selection": {
        "tagStatus": "tagged",
        "tagPrefixList": [
          "QA-3"
        ],
        "countType": "imageCountMoreThan",
        "countNumber": 7
      },
      "action": {
        "type": "expire"
      }
    },
    {
      "rulePriority": 8,
      "description": "Remove imagens com TAG qa-automacao > 5",
      "selection": {
        "tagStatus": "tagged",
        "tagPrefixList": [
          "QA-AUTOMACAO"
        ],
        "countType": "imageCountMoreThan",
        "countNumber": 5
      },
      "action": {
        "type": "expire"
      }
    },
    {
      "rulePriority": 9,
      "description": "Remove imagens com TAG RC > 5",
      "selection": {
        "tagStatus": "tagged",
        "tagPrefixList": [
          "RC"
        ],
        "countType": "imageCountMoreThan",
        "countNumber": 5
      },
      "action": {
        "type": "expire"
      }
    },
    {
      "rulePriority": 10,
      "description": "Remove imagens com TAG SB > 5",
      "selection": {
        "tagStatus": "tagged",
        "tagPrefixList": [
          "SB"
        ],
        "countType": "imageCountMoreThan",
        "countNumber": 5
      },
      "action": {
        "type": "expire"
      }
    },
    {
      "rulePriority": 11,
      "description": "Remove imagens com HML-CLIENT",
      "selection": {
        "tagStatus": "tagged",
        "tagPrefixList": [
          "HML-CLIENT"
        ],
        "countType": "imageCountMoreThan",
        "countNumber": 7
      },
      "action": {
        "type": "expire"
      }
    }
  ]
}

        policy_jason = json.dumps(lifecycle_policy)

        try:
            response = ecr.put_lifecycle_policy(
                repositoryName = repo_name,
                lifecyclePolicyText = policy_jason
            )
            
            print("Lifecycle Policy aplicada com sucesso no repo:" f"{repo_name}")

        except Exception as e:
            print(f"Erro ao aplicar Lifecycle Policy: {e}")

        qtd_repos += 1

        
    return qtd_repos



# Valida repositórios no geral
response = ecr.describe_repositories(maxResults=411)
qtd_repos = 0
qtd_repos = get_repos(response)
print(qtd_repos)

# with open('teste.csv', 'w') as csvfile:
#     writer = csv.writer(csvfile, delimiter= ',')
#     writer.writerow(['NOME', 'creatData', 'lifecycle', 'SIZE', 'lastImage', 'lastRecordedPullTime'])
#     for arq2 in list_repo:
#         str1 = str(arq2.storage) + 'GB'
#         writer.writerow([arq2.nome, arq2.creatData, arq2.lifecycle, str1, arq2.lastImage, arq2.lastRecordedPullTime])

# print("\nQuantidade de repositórios: ", qtd_repos)
