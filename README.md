# Let AI Control Your Terminal

This is a simple script that allows you to type in a simple prompt into it, and the ai will use your terminal to execute all of the commands you need to make your request happen.

It does have a bit of setup, which is to execute these commands in your project directory.
(PS This only works on MacOS for now windows support will be soon.)

```
git clone https://github.com/WhatsindatNamebo/local-terminal-control.git
cd local-terminal-control
```
This clones the repo then moves your terminal into the new repo folder.
Next, you need to install a virtual python enviorment.
```
python3 -m venv venv
```
Next activate the environment
```
source venv/bin/activate
```
Next install the python requirements
```
pip install ollama pexpect httpx
```
Then, you will need to install ollama, which you can do with [this link](https://ollama.com/download)
Next, select your operating system.
When it is done installing, go back to your terminal and type in
```
ollama --version
```
This command should give an output that looks a bit like this:
```
YourUsername@YourHostname local-terminal-control % ollama --version
ollama version is 0.9.3
```
After that is installed, you need to install minstral, or any other model you might want to use form ollama.
To install the model, use this command
```
ollama pull minstral
```
Once you have finished downloading the model, it is now time to run the script.
To do that, enter this into your terminal
```
python main.py
```
and now you can begin using your new AI terminal!

## For more information
You can see my youtube channel for more information and an explination on how it all works.
My youtube channel: [Byte Snatcher Codes](https://www.youtube.com/@ByteSnatcherCodes)
