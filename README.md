# SDN-Power-Optimization
An Adaptive Routing Framework for Efficient Power Consumption in Software-Defined Datacenter Networks
This project represents the work in our paper submitted to [10th Anniversary of Electronics: Advances in Networks](https://doi.org/10.3390/electronics10233027) "An Adaptive Routing Framework for Efficient Power Consumption in Software-Defined Datacenter Networks",  DOI: [10.3390/electronics10233027](https://doi.org/10.3390/electronics10233027), Authors: Mohammed Nsaif, Gergely Kovásznai, Anett Rácz, Ali Malik and Ruairí de Fréin

### In this project, we provide:

- Part of the code of the paper. More details will be provided as soon as possible

### Dependencies

#### OS: Ubuntu 20.04.x

>  If you are using Windows or other OS, you can install Ubuntu 20.04 as a Virtual Machine (VM) using Virtual Box. You can download the ISO installer from this [link:](https://www.ubuntu.com/download/desktop)

####  Ryu controller

> We use [POX](https://github.com/noxrepo/pox) to deploy our management and monitoring SDN application. POX can work in any OS Environment that supports Python 2 or 3. You can install pox as follows:
```
git clone http://github.com/noxrepo/pox
```

#### Mininet

> To simulate an SDN network, we use the popular framework [Mininet](http://mininet.org/). Mininet currently only works in Linux. In our project, we run mininet in an Ubuntu 20.04.2 LTS VM. To get mininet, you can simply download a compressed Mininet VM from [Mininet downloadpage](https://github.com/mininet/mininet/wiki/Mininet-VM-Images) or install it through apt: 
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
A collection of guides detailing how to install Open vSwitch in a variety of different environments and using different configurations can be found here](https://docs.openvswitch.org/en/latest/intro/install/). However, for Ubuntu as follows:

```
sudo apt-get install openvswitch-switch
```

#### Distributed Internet Traffic Generator
> D-ITG is a platform capable of producing traffic at the packet level accurately replicating appropriate stochastic processes for both IDT (Inter Departure Time) and PS (Packet Size) random variables (exponential, Uniform, Cauchy, Normal, Pareto, ...).
D-ITG supports both IPv4 and IPv6 traffic generation and it is capable of generating traffic at the network, transport, and application layer.
Install and usage guidelines, you can be found [here](https://traffic.comics.unina.it/software/ITG/)

> Quique installation as follows:

```
sudo apt-get install D-ITG
```


### SDN Applications Usage

In this project, we created two Ryu applications, and the source codes are stored in the  [SDN-Power-Optimization directory](https://github.com/nsaif86/SDN-Power-Optimization/tree/main). The first component, FPLF, is responsible for consolidating the flows in the one-link as much as possible. The second is data Center Network topology. The method is clearly described in our paper.



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

See this [video](https://www.youtube.com/watch?v=VcedqMK4RPU), which includes a practical example of running the code. Please, if you find the code useful, cite our work.

to cite :

@article{nsaif2021adaptive,
  title={An adaptive routing framework for efficient power consumption in software-defined datacenter networks},
  author={Nsaif, Mohammed and Kov{\'a}sznai, Gergely and R{\'a}cz, Anett and Malik, Ali and de Fr{\'e}in, Ruair{\'\i}},
  journal={Electronics},
  volume={10},
  number={23},
  pages={3027},
  year={2021},
  publisher={MDPI}
}
