# Publication comics in VK

this code allows you to publish random comics from the [site by Randel Munro](https://xkcd.com/) to your group in [VK](https://vk.com)

### How to install

Python3 should be already installed.
Then use `pip` (or `pip3`, if there is a conflict with Python2) to install dependencies:
```
pip install -r requirements.txt
```
To automatically publish a post, the code uses the VK app you must click create on [this site](https://vk.com/apps?act=manage). Then you need to get the `client_id` of the application for this on the same page, after creating the application, click on edit, then go to the settings and copy the *application id*. After you have recognized the `client_id` in the folder with the code, create a file called `.env`, write `CLIENT_ID=your_client_id` in the file.After we need an `ACCESS_TOKEN`, for this we need to change the value after `CLIENT_ID` in this link:
```
https://oauth.vk.com/oauth/authorize?client_id=8213967&response_type=token&scope=photos,groups,offline,wall
```
to the one we received, follow this link, give permission, after you will be transferred to the page, in its link there will be an `access_token=` and copy everything up to the & sign. After that, in the `.env` file, write `ACCESS_TOKEN=your_access_token`. Well, it remains only to create a group, for this, follow this link and click create a community, after you have created a community, go to the community page and copy the *NUMBERS* after the club in the link. After in our `.env` file we create `GROUP_ID=your_group_ID`. In addition, if you have a version error, you can create in .env specify the version of vk api API_VERSION=

### How to run
To run the program itself, you need to write the following command on the command line:
```
python main.py 
```
