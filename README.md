Grading rubric for the final presentation:

100 points possible:

+15 - Application is demonstrated with functionality (3rd party API included)

+15 - Application is running in the cloud (on AWS)

+20 - Application is running in Docker (not outside)

+10 - Secrets are stored in Doppler, and Doppler is being used in the action

+15 - Unit tests demonstrated and 80% coverage is achieved and shown

+15 - GitHub Actions are used with at least the following 3 jobs (5 points each):

    Test stage that runs unit tests on the code (does not have to prove coverage, just that tests pass)
    Build stage that creates a Dockerfile and pushes it up to Docker Hub
    Deploy stage that pulls the image down from Docker Hub and runs the container in AWS
    Extra Credit +10 if you add a fourth job that does something else special

+10 - PowerPoint or other presentation software that does the following:

    Describes the problem being solved
    Describes the tech stack
    Describes challenges or pivots made
    Everyone on the team participates in the presentation
    Between 10 and 15 minutes (lose points if wildly outside this range)
