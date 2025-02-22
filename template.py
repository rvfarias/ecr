import boto3

session = boto3.Session(profile_name="", region_name="us-east-1")
ecr = session.client("ecr")


def get_repos_about_lifecycle_policy(response):
    qtd_repos = 0
    qtd_repo_with_lifecycle_policy = 0
    qtd_repo_without_lifecycle_policy = 0
    for repo in response["repositories"]:
        try:
            #lifecycle_policy = ecr.get_lifecycle_policy(repositoryName=repo["repositoryName"])
            #ecr_with_lifecycle_policy.append(repo["repositoryName"])
            qtd_repo_with_lifecycle_policy += 1
        except ecr.exceptions.LifecyclePolicyNotFoundException:
            #ecr_without_lifecycle_policy.append(repo["repositoryName"])
            qtd_repo_without_lifecycle_policy += 1

        qtd_repos += 1

    return qtd_repos, qtd_repo_with_lifecycle_policy, qtd_repo_without_lifecycle_policy#, ecr_with_lifecycle_policy, ecr_without_lifecycle_policy

# Valida repositórios no geral
response = ecr.describe_repositories(maxResults=411)

# Valida lifecycle policy
# ecr_with_lifecycle_policy = []
# ecr_without_lifecycle_policy = []
qtd_repos = 0
qtd_repo_with_lifecycle_policy = 0
qtd_repo_without_lifecycle_policy = 0

qtd_repos, qtd_repo_with_lifecycle_policy, qtd_repo_without_lifecycle_policy = get_repos_about_lifecycle_policy(response)
print(f"\nQuantidade de repositórios: {qtd_repos}")
print(f"Quantidade de repositórios com lifecycle policy: {qtd_repo_with_lifecycle_policy}")
print(f"Quantidade de repositórios sem lifecycle policy: {qtd_repo_without_lifecycle_policy}")

# Valida repositório com muitas imagens
# ecr_with_many_images = [] # Maior que 15

# for repo in response["repositories"]:
#     images = ecr.list_images(repositoryName=repo["repositoryName"])
#     if len(images["imageIds"]) > 15:
#         ecr_with_many_images.append(repo["repositoryName"])

# print(f"Quantidade de repositórios com muitas imagens: {len(ecr_with_many_images)}")
