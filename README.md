**DFS-Pub-Sub**  
DFS-Pub-Sub is a distributed file system implementation utilizing a publish-subscribe (pub-sub) communication model. This project aims to provide a scalable and fault-tolerant file storage solution with asynchronous message passing between nodes.
  
**Features**   
Distributed File Storage: Efficiently stores files across multiple nodes with no single point of failure.  
Publish-Subscribe Communication: Implements a pub-sub model for messaging, ensuring decoupled and asynchronous communication.  
Scalability: Easily scales to handle large volumes of data and nodes.  
Fault Tolerance: Ensures data availability and integrity even in the event of node failures.  

**Getting Started**  
Follow these instructions to set up and run the DFS-Pub-Sub system on your local machine for development and testing purposes.  
  
**Prerequisites**
  Python 3.8+  
  pip  
  Git  
  
**Installation** 
  
1. Clone the repository:  
  
    git clone https://github.com/kdheerajreddy97/DFS-Pub-Sub.git
    cd DFS-Pub-Sub  
  
2. Create a virtual environment and activate it:
     
    python3 -m venv venv  
    source venv/bin/activate   # On Windows use `venv\Scripts\activate`  
    
3. Install the required packages:  
  
    pip install -r requirements.txt  

      
**Running the Application**

1. Start the DFS-Pub-Sub nodes:  
  
    python dfs_pub_sub_node.py  
    
2. Use the provided client application to interact with the file system:  
  
    python dfs_pub_sub_client.py  
    
**Usage**  
  
1. Storing a File:  
  
    from dfs_client import DFSClient  
    dfs_client = DFSClient()  
    dfs_client.store_file("path/to/your/file.txt")  
  
2. Retrieving a File:  
  
    from dfs_client import DFSClient  
    dfs_client = DFSClient()  
    retrieved_file = dfs_client.retrieve_file("file.txt")


**Team Members:**  
Dheeraj Reddy Kukkala  
Venkatesh Meesala  
