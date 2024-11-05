# 2024 TAMUHack IEEE Hardware Challenge Submission: 
## An Artificial Intelligence/Machine Learning (AI/ML)-assisted Multi-factor authentication (MFA) System

### Inspiration

Voice phishing is a very prominent scam that can attack anyone, no matter how secure.
### What it does

The system integrates advanced hardware and software components for secure audio verification. A USB is plugged into a device where the system prompts the user to put in their credentials (username and password) and then record a short message that is then compared to a pre-existing audio recording of the user collected during the system set up process. The system checks if the voice is the individual's, and ensures that the voice is not AI-generated. Once the user passes these checks, they are allowed in to the system/application of their choice.
### How we built it

The hardware setup for audio verification involves the use of a Raspberry Pi and a hardware key. The Raspberry Pi serves as the central processing unit for running the back end and managing databases. It is connected to the user's computer, and a hardware key can be plugged into the computer for voice recognition. This key acts as a tangible authentication device for audio verification. When the user attempts verification, the hardware key conducts voice recognition tests to determine authentication status. Successful authentication grants access to the system. The software infrastructure relies on Automatic Speech Recognition (ASR) technology patented by NVIDIA NeMo. For web development, Flask is employed to handle the back-end processes, including database management. Users interact with the system through a web interface, where they are prompted to enter a password and record an audio sample for verification. The recorded audio is processed using the pre-trained machine learning model using ASR technology to validate the user's identity. Validation is done by checking the audio recording of the user with a pre-recorded audio that was stored during account set up. The authentication process is also extended to a hardware key, which, when plugged into the computer, conducts voice recognition tests to ensure that the user is authorized. The combination of ASR, Flask, and hardware-based authentication provides a robust solution for audio verification.
### Challenges we ran into

A big issue we ran into was how long it took for the pre-trained machine learning models to actually be processed on the OS, and the incompatibility between the MacOS and the models. Furthermore, switching laptops to a Linux OS also came with its own issues such as slower processing, which hindered our progress significantly. Using the Raspberry Pi also occasionally proved to be a challenge as we had to scramble for a connector between the Raspberry Pi and the laptop. Furthermore, the Raspberry Pi would be close to burning out as it was not equipped to handle the amount of data processing we were making it do.
### Accomplishments that we're proud of

Getting our Raspberry Pi to connect and interact with our laptop system proved to be our greatest feat, and we were excited to see the Raspberry Pi interact with the user prompts.
### What we learned

We learned how to troubleshoot different OS, working around restraints that come with combining incompatible hardware and software, and working as a team to exchange and brainstorm ideas.
### What's next for Voice Authentication System

We hope to fine tune our audio verification by using our own trained models, and possibly creating a better user interface to test the system through our own application. We also hope to add a facial recognition aspect.
