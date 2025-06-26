import uuid

def generate_unique_id():
    unic_id = str(uuid.uuid4())
    unic_id = unic_id.replace("-", "_")
    return unic_id

# if __name__ == "__main__":
#     print(generate_unique_id())