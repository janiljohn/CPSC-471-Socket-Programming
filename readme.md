# Project README

## Group Members:
- Joel Anil John (Email: joel.aniljohn@csu.fullerton.edu)
- Indrajeet Patwardhan (Email: Indrajeet2002@csu.fullerton.edu)
- Danyal Nemati (Email: dnemati@csu.fullerton.edu)
- Abe Oueichek (Email: abeo@csu.fullerton.edu)
- Zeid Zawaideh

## Project Overview:
This project is implemented in Python and involves a server-client architecture.

## How to Execute the Program:

1. **Run the Server:**
   - Execute the `server.py` file to start the server.
     ```bash
     python server.py
     ```
     or
     ```bash
     python3 server.py
     ```

2. **Establish Connection to Server:**
   - Run the `cli.py` file to establish a connection to the server. Specify the server address and the server portnumber as arguments like shown below:
     ```bash
     python cli.py localhost 1234
     ```
     or
     ```bash
     python3 cli.py localhost 1234
     ```
   - Replace `localhost` with the server address and `1234` with the port number if needed.

3. **Run FTP Commands:**
   - Now that the server and the client are up and running, any of the below four commands can be run:
     ```bash
     get <file name> (downloads file <file name> from the server)
     put <filename> (uploads file <file name> to the server)
     ls (lists files on theserver)
     quit (disconnects from the server and exits)
     ```

4. **Sample Files:**
   - The ./sendfile director contains two sample file that can be used as files to upload when running the "put" command.
   - Make sure to specify the director that these files are in before using them. For example:
   ```bash
   put ./sendfile/file.txt
   ```
   or
   ```bash
   put ./sendfile/test.txt
   ```