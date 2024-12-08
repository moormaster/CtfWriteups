Title: General Skills / Binary Search
Date: 2024-12-07

We are provided a game script that automatically gets executed when connecting to the remote shell:

    :::bash linenums=False
    #!/usr/bin/bash

    # Generate a random number between 1 and 1000
    target=$(( (RANDOM % 1000) + 1 ))

    echo "Welcome to the Binary Search Game!"
    echo "I'm thinking of a number between 1 and 1000."

    # Trap signals to prevent exiting
    trap 'echo "Exiting is not allowed."' INT
    trap '' SIGQUIT
    trap '' SIGTSTP

    # Limit the player to 10 guesses
    MAX_GUESSES=10
    guess_count=0

    while (( guess_count < MAX_GUESSES )); do
        read -p "Enter your guess: " guess

        if ! [[ "$guess" =~ ^[0-9]+$ ]]; then
            echo "Please enter a valid number."
            continue
        fi

        (( guess_count++ ))

        if (( guess < target )); then
            echo "Higher! Try again."
        elif (( guess > target )); then
            echo "Lower! Try again."
        else
            echo "Congratulations! You guessed the correct number: $target"

            # Retrieve the flag from the metadata file
            flag=$(cat /challenge/metadata.json | jq -r '.flag')
            echo "Here's your flag: $flag"
            exit 0  # Exit with success code
        fi
    done

    # Player has exceeded maximum guesses
    echo "Sorry, you've exceeded the maximum number of guesses."
    exit 1  # Exit with error code to close the connection

The task is to implement a script that reads the output of the shell and implements binary search to find the correct answer.

To connect stdin & stdout of a script with stdout & stdin of another command (i.e. a remote shell) one can use [coproc](https://www.gnu.org/software/bash/manual/html_node/Coprocesses.html)

    :::bash
    coproc A { echo "hello from proc A"; read a; echo "proc A received: $a" >&2; }
    { echo "hello from proc B"; read a; echo "proc B received: $a" >&2; } <&${A[0]} >&${A[1]}

output:

    proc B received: hello from proc A
    proc A received: hello from proc B

so we first build ourselves a helper script to connect stdin/stdout of two commands using `coproc`.

coproc-connect.sh

    :::bash linenums=False
    #!/bin/bash

    if [ $# -ge 2 ]
    then
        script="$1"
        shift
        coproc A { "$@"; }

        echo "Giving 5s time to enter ssh password.."
        sleep 5

        "$script" <&${A[0]} >&${A[1]}
    else
        echo "Usage: $0 <script1> <command>"
    fi

Now we can use that helper script for both

- testing a local binary-search implementation against the local `guessing-game.sh`
- running a local binary-search implementation against the remote shell

What we are still missing is the binary-search implementation, so lets create one.

    :::bash linenums=False
    #!/bin/bash

    upper_bound=1000
    lower_bound=1

    candidate=500

    # receive and echo welcome messages from game
    read welcome_message; echo "<- $welcome_message" >&2
    read welcome_message; echo "<- $welcome_message" >&2

    while true
    do
        # send and echo (next) answer
        echo "${candidate}"; echo "-> ${candidate}" >&2

        # receive and echo response
        read response; echo "<- $response" >&2
        if echo "$response" | grep -q "Higher"
        then
            lower_bound=${candidate}
        elif echo "$response" | grep -q "Lower"
        then
            upper_bound=${candidate}
        else
            break
        fi

        # calculate next candidate answer in the middle between lower and upper bounds
        candidate=$(( ${lower_bound}+(${upper_bound}-${lower_bound})/2 ))
    done

    # receive and echo flag
    read flag; echo "$flag" >&2

A small test against the local `./guessing_game.sh` proves that the solution works

    :::text
    $ ./coproc-connect.sh ./solution.sh home/ctf-player/drop-in/guessing_game.sh 
    Giving 5s time to enter ssh password..
    <- Welcome to the Binary Search Game!
    <- I'm thinking of a number between 1 and 1000.
    -> 500
    <- Lower! Try again.
    -> 250
    <- Higher! Try again.
    -> 375
    <- Higher! Try again.
    -> 437
    <- Lower! Try again.
    -> 406
    <- Congratulations! You guessed the correct number: 406
    home/ctf-player/drop-in/guessing_game.sh: Zeile 37: jq: Kommando nicht gefunden.
    cat: /challenge/metadata.json: Datei oder Verzeichnis nicht gefunden
    406

Running it against the remote shell will replace the error message with the flag of the challenge:

    :::text
    $ ./coproc-connect.sh ./solution.sh ssh -p 60545 ctf-player@atlas.picoctf.net
    Giving 5s time to enter ssh password..
    Pseudo-terminal will not be allocated because stdin is not a terminal.
    ctf-player@atlas.picoctf.net's password: 
    <- Welcome to the Binary Search Game!
    <- I'm thinking of a number between 1 and 1000.
    -> 500
    <- Lower! Try again.
    -> 250
    <- Lower! Try again.
    -> 125
    <- Lower! Try again.
    -> 63
    <- Higher! Try again.
    -> 94
    <- Higher! Try again.
    -> 109
    <- Congratulations! You guessed the correct number: 109
    Here's your flag: picoCTF{...}
