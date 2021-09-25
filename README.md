
# Reverse Polish Notation Calculator
### v. 1.1

&nbsp;

## Description -

This is an interactive command line program for users to calculate a Reverse Polish Notation expression.

&nbsp;

## Reasoning -

This initially started off as a Python [curses](https://docs.python.org/3/library/curses.html) program, but some of the quirks associated with the library began to add up.  (Norally, I develop things on a Windows platform, so shifting over to development/testing with Linux was interesting.)

Due to some challenges with the [curses](https://docs.python.org/3/library/curses.html)  library, the initial program was put on the backburner and the one that you'll be using was developed using the [cmd](https://docs.python.org/3/library/cmd.html) standard library for Python.

&nbsp;

## How-To:

From UNIX/Linux terminal - 

1. Clone repo to local drive
2. `cd` into `rpn_exercise`
3. Run the following from the command line:

```bash
$ ./launch-rpn.sh
```

Once launched, you can type `help` to see a list of available commands.  Typing `help [command]` will bring up more information.

To quit the program, type `q` or `exit`.

&nbsp;

## Testing

To run unittests, from the root folder in your cloned instance, run:

```bash
$ ./run-tests.sh
```

&nbsp;

## Documentation

There's also the ability to view pydoc documentation.  From your bash terminal, run the following:

```bash
$ ./view-docs.sh
```

This will genrate documentation into the ./rpn/docs folder and start a simple server for the local address: [http://127.0.0.1:9876](http://127.0.0.1:9876)

Users are more than welcome to change that port number or anything else they'd like to about the server.

---

<details>
<summary>References (partial):</summary>
<ul>
    <li><a href="https://leachlegacy.ece.gatech.edu/revpol/" target="_blank" style="color:#61a7c8;">Georgia Tech</a></li>
    <li><a href="https://docs.python.org/3.7/library/cmd.html" target="_blank" style="color:#61a7c8;">Python 3.7: Cmd</a></li>
    <li><a href="https://en.wikipedia.org/wiki/ANSI_escape_code" target="_blank" style="color:#61a7c8;">ANSI escape code (Wikipedia)</a></li>
</ul>
</details>
