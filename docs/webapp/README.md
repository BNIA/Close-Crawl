# Usage

One of the major requirements for Close Crawl was a friendly and non-technical UI/UX configuration. As a reminder, the production version of the project can be summarized as a local web application executed by a single file standing on less than 24 MB of hard drive space. The goal is to allow the end users to avoid any installation of prerequisite software or other technical configuration.

This version is considered unstable and in production. Use the command line interface version of the executable for accurate outputs.

<img src="https://raw.githubusercontent.com/BNIA/Close-Crawl/master/docs/webapp/demo.gif">
<sup>Demo Displaying v0.9.6</sup>

## Executable

For the production version, only the contents in the `dist` folder are required. The rest of the repository can be safely removed if they are not being used for development.

Once the executable file is run, a terminal pops up displaying the status of the server along with its address. It is currently set to run on port 9000, but future updates may support an option for a port chosen by the user.

## Navigation

**NOTE: The project has been developed and tested on Google Chrome browsers. Templates may not load or function properly in different browsers.**

Navigate to the address of the server (either 127.0.0.1:PORT or localhost:PORT). If templates load on the browser, navigate to the parameters for scraping the cases. The parameters function as follows:
- `File Name (text input)` is the name of the output CSV file. All the cases crawled and scraped will be stored in this file. The output should be located in the same directory as the executable.
- `Year (dropdown)` is the year of the cases to be scraped
- `Type (radio)` is the type of cases to be scraped
- `Lower Bound (slider/numeric input)` is the lower bound of the range of cases
- `Upper Bound (slider/numeric input)` is the upper bound of the range of cases
- `Debug (checkbox)` is the option for Debug Mode. During the entire process, many files are created temporarily and removed once the final clean dataset is created. Debug Mode keeps the temporary files and other logs for further inspection.

Example: with the following parameters:
  ```
  [File Name]=demo.csv
  [Year]=2016
  [Type]=Mortgage
  [Lower Bound]=1
  [Upper Bound]=50
  [Debug]=off
  ```
the cases 24O16000001 through 24O16000050 will be scraped and saved to a file named `demo.csv` without any additional temporary files or logs.

Once the parameters are selected and the process is executed, the progress can be displayed on the terminal. The templates and the log on the terminal will indicate the termination of the process.

It is important that the server is shut down when not in use so as to prevent any chances of a deadlock.