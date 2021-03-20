# Space Instagram

[![50631642722-3af8131c6f-o.jpg](https://i.postimg.cc/9M0prpgv/50631642722-3af8131c6f-o.jpg)](https://postimg.cc/ZBk3QrSc)

Application allows:
1. Downloading SpaceX last launch images
2. Downloading Hubble images belonging to a specific collection
3. Resizing images to Instagram format
4. Post images on Instagram

## How to install
Python3 and Git should be already installed. 

1. Clone the repository by command:
```console
git clone https://github.com/balancy/space_instagram
```
2. Inside cloned repository create virtual environment by command:
```console
python -m venv env
```
3. Activate virtual environment. For linux-based OS:
```console
source env/bin/activate
```
&nbsp;&nbsp;&nbsp;&nbsp;For Windows:
```console
env\scripts\activate
```
4. Install dependencies:
```
pip install -r requirements.txt
```
5. Rename file `.env.example` to `.env` and initialize your instagram username and password
```console
INSTAGRAM_USERNAME = 'your_instagram_username'
INSTAGRAM_PASSWORD = 'your_instagram_password'
```
## Project Goals
The code is written for educational purposes on online-course for web-developers dvmn.org.