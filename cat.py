import boto3, csv
from datetime import datetime, timezone

session = boto3.Session(profile_name="", region_name="us-east-1")
ecr = session.client("ecr")

def bytes_for_gb(bytes):
    divisor = 1024**3
    return bytes/divisor

def return_images_infos(repositoryName):
    ## Verifica lifecycle policy
    has_lifecycle_policy = False
    try:
        ecr.get_lifecycle_policy(repositoryName=repositoryName)
        has_lifecycle_policy = True
    except ecr.exceptions.LifecyclePolicyNotFoundException:
        has_lifecycle_policy = False

    ## Verifica repositorio created date
    response = ecr.describe_repositories(repositoryNames=[repositoryName])
    created_data = response['repositories'][0]['createdAt']

    ## Verifica imagens last pull
    images = ecr.describe_images(repositoryName=repositoryName, maxResults=50)
    last_pull_date = datetime(1970, 1, 1, tzinfo=timezone.utc)
    last_image_pull_tag = []

    for image in images['imageDetails']:
        last_pull_date_candidate = image.get('lastRecordedPullTime', last_pull_date)
        last_image_pull = image.get('imageTags', last_image_pull_tag)
        if last_pull_date_candidate > last_pull_date:
            last_pull_date = last_pull_date_candidate
            last_image_pull_tag = last_image_pull

    ## Verifica imagens last pushed
    last_pushed_date = datetime(1970, 1, 1, tzinfo=timezone.utc)
    image_tags = []

    for image in images['imageDetails']:
        last_pushed_date_candidate = image.get('imagePushedAt', last_pushed_date)
        image_tag = image.get('imageTags', image_tags)
        if last_pushed_date_candidate > last_pushed_date:
            last_pushed_date = last_pushed_date_candidate
            image_tags = image_tag

    if last_pushed_date == datetime(1970, 1, 1, tzinfo=timezone.utc):
        last_pushed_date = None


    ## Verifica tamanho das imagens
    size = 0
    for image in images['imageDetails']:
        size += image['imageSizeInBytes']

    dt_naive = last_pull_date.replace(tzinfo=None, microsecond=0)

    return size, dt_naive, last_image_pull_tag, has_lifecycle_policy, created_data, last_pushed_date, image_tags

response = ecr.describe_repositories(maxResults=411)
total_ecr_size = 0
dados = []
for repo in response['repositories']:
    size, dt_naive, last_image_pull_tag, has_lifecycle_policy, created_data, last_pushed_date, last_image_tags = return_images_infos(repo['repositoryName'])
    total_ecr_size += size

    gb_size = bytes_for_gb(size)

    # print(f"Repo: {repo['repositoryName']}")
    # print(f"HasLifecyclePolicy: {has_lifecycle_policy}")
    # print(f"LastImagePushed: {last_pushed_date}")
    # print(f"LastTagImagePushed: {last_image_tags}")
    # print(f"CreatedAt: {created_data}")
    # print(f"LastPull: {last_pull_date}")
    # print(f"LastImagePull: {last_image_pull_tag}")
    # print(f"Size: {gb_size:.2f} GB\n\n")

    dados.append({
        'repositoryName': repo['repositoryName'],
        'has_lifecycle_policy': has_lifecycle_policy,
        'last_image_pushed': last_pushed_date,
        'last_tag_image_pushed': last_image_tags,
        'created_data': created_data,
        'last_pull_date': dt_naive,
        'last_image_pull_tag': last_image_pull_tag,
        'size': f"{gb_size:.2f}"
    })

print(f"Total ECR Size: {total_ecr_size:.2f} GB")

with open('RPE-NEWPROD.csv', 'w', newline='') as file:
    fieldnames = ['repositoryName', 'has_lifecycle_policy', 'last_image_pushed', 'last_tag_image_pushed', 'created_data', 'last_pull_date', 'last_image_pull_tag', 'size']
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(dados)

print("CSV criado com sucesso!")