# Development Environment Setup
## Manual Install

1. Install Python 3, Ruby, and NodeJS.
2. Clone this repository:

       git clone git@github.com:google/wireless-debugging.git

3. `cd` to the `server` directory.
4. Install the necessary Ruby gems (for SASS):

       gem install compass font-awesome-sass bootstrap-sass

5. Install the necessary Python libraries. You can use `pip3 install -r
   requirements.txt` or use the following command:

       pip3 install requirements.txt

6. Install the necessary NodeJS tools:

       nmp install

7. Run `compass compile` to compile the SASS to CSS.

8. Run `./widb_server.py` (you may have to prepend `sudo` to bind to port 80)
   and go to `localhost` in your browser.

## With Docker Compose
**Note:** you might need to run some of these commands using `sudo`.
1. Install [Docker Compose](https://docs.docker.com/compose/install/): `pip
   install docker-compose`.
2. Clone the repository.
3. Run `docker-compose build`
4. Run `docker-compose up`

## Where to go from Here
- Understand the [Project Structure](Project-Structure)
- Learn how to [Run Tests](Running-Tests)
