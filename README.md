## Project Setup (ndk-proj2)

### Prerequisites

1. **AWS CLI:** Download and install the AWS CLI from the official documentation: [https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
2. **Docker:** Download and install Docker Desktop for deploying the image: [https://www.docker.com/](https://www.docker.com/)

### AWS Configuration

1. Configure your AWS credentials using `aws configure` in your terminal. You will need to provide your AWS Access Key ID, Secret Access Key, and Region. 
    * Region: `us-east-1` (**Replace if using a different region**)
    * Access Key ID: `[your_access_key_id]` (**Replace with your actual key ID**)
    * Secret Access Key: `[your_secret_access_key]` (**Replace with your actual secret key**)

### Code Setup

1. **Git Clone:** Clone the project repository and navigate to the project directory.

**Optional Changes :**

1. **Dockerfile:** Add a line `COPY encoding /home/app/` to the Dockerfile.
2. **requirements.txt:** Change `ffmpeg` to `python-ffmpeg` in the requirements.txt file.

### Building and Deploying the Docker Image

1. **Login to ECR:** Obtain the login password for your ECR repository using:

   ```bash
   aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 458362110587.dkr.ecr.us-east-1.amazonaws.com
   ```

   **Replace the highlighted section with your specific ECR registry information.**

2. **Build the Image:** Build the docker image with the following command:

   ```bash
   docker build -t proj2-docker-lambda .
   ```

3. **Tag the Image:** Tag the built image for your ECR repository:

   ```bash
   docker tag proj2-docker-lambda:latest 458362110587.dkr.ecr.us-east-1.amazonaws.com/proj2-docker-lambda:latest
   ```

   **Replace the highlighted section with your specific ECR registry information.**

4. **Push the Image:** Push the tagged image to your ECR repository:

   ```bash
   docker push 458362110587.dkr.ecr.us-east-1.amazonaws.com/proj2-docker-lambda:latest
   ```

   **Replace the highlighted section with your specific ECR registry information.**

### Uploading Data (Optional)

1. **Upload Database (if needed):** Run `python3 uploadDB.py` to populate the database table (`ndk-proj2-table`). This step might not be required if the table is already populated.

2. **Upload Videos:** Run `python3 workload.py` to upload the videos in the `test` folder to the S3 bucket named `ndk-proj2input`.

**Note:** Replace placeholders like `[your_access_key_id]` and `[your_secret_access_key]` with your actual AWS credentials. Additionally, replace any highlighted sections with your specific ECR registry information if it differs from the example.
