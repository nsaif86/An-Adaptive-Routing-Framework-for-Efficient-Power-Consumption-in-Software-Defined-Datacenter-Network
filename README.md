# SDN-Power-Optimization
An Adaptive Routing Framework for Efficient Power Consumption in Software-Defined Datacenter Networks
This project represents the work in our paper submitted to [10th Anniversary of Electronics: Advances in Networks](https://doi.org/10.3390/electronics10233027) "An Adaptive Routing Framework for Efficient Power Consumption in Software-Defined Datacenter Networks",  DOI: [10.3390/electronics10233027](https://doi.org/10.3390/electronics10233027), Authors: Mohammed Nsaif, Gergely Kovásznai, Anett Rácz, Ali Malik and Ruairí de Fréin

### In this project, we provide:

- Part of the code of the paper. More details will be provided as soon as possible

### Dependencies

#### OS: Ubuntu 20.04.x

>  If you are using Windows or other OS, you can install Ubuntu 20.04 as a Virtual Machine (VM) using Virtual Box. You can download the ISO installer from the this [link:](https://www.ubuntu.com/download/desktop)

####  Ryu controller

> We use [POX](https://github.com/noxrepo/pox) to deploy our management and monitoring SDN application. POX can work in any OS Environment that support python 2. You can install pox as following:
```
git clone http://github.com/noxrepo/pox
```

#### Mininet

> To simulate an SDN network, we use the popular framework [Mininet](http://mininet.org/). Mininet currenttly only works in Linux. In our project, we run mininet in an Ubuntu 20.04.2 LTS VM. To get mininet, you can simply download a compressed Mininet VM from [Mininet downloadpage](https://github.com/mininet/mininet/wiki/Mininet-VM-Images) or install through apt: 
```
sudo apt update 
sudo apt install mininet
```
> or install natively from source:
```
git clone git://github.com/mininet/mininet
cd mininet
git tag  # list available versions
git checkout -b cs244-spring-2012-final  # or whatever version you wish to install
util/install.sh -a
```

#### Openvswitch Installation: 
A collection of guides detailing how to install Open vSwitch in a variety of different environments and using different configurations can find [here](https://docs.openvswitch.org/en/latest/intro/install/). However, for ubuntu as follows:

```
sudo apt-get install openvswitch-switch
```

#### Distributed Internet Traffic Generator
> D-ITG is a platform capable to produce traffic at packet level accurately replicating appropriate stochastic processes for both IDT (Inter Departure Time) and PS (Packet Size) random variables (exponential, uniform, cauchy, normal, pareto, ...).
D-ITG supports both IPv4 and IPv6 traffic generation and it is capable to generate traffic at network, transport, and application layer.
Install and usage guidelines, you can be found [here](https://traffic.comics.unina.it/software/ITG/)

> Quique installation as following:

```
sudo apt-get install d-itg
```


### SDN Applications Usage

In this project, we created two Ryu applications, and the source codes are stored in the  [SDN-Power-Optimization directory](https://github.com/nsaif86/SDN-Power-Optimization/tree/main). The first component, FPLF, is responsible for consolidation the flows in the one like as much as posable. The second, Data Center Network topology. The method is clearly described in our paper.



To run the applications, copy the two Python programs into the pox.ext folder of the pox directory and open two terminal windows, execute the following command:

In the first terminal
```
sudo ./pox.py  openflow.discovery FPLF

```
In the second terminal
```
sudo python topology.py
```
Then, you can generate traffic (voice, DDoS, etc.) using D-ITG inside Mininet and observe the results in the second terminal.

More files and descriptions will be available as soon as possible. Please, if you find the code useful, cite our work.

to cite :

Nsaif, M.; Kovásznai, G.; Rácz, A.; Malik, A.; de Fréin, R. An Adaptive Routing Framework for Efficient Power Consumption in Software-Defined Datacenter Networks. Electronics 2021, 10, 3027. https://doi.org/10.3390/electronics10233027
