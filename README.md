# CXO Free Me

This tool releases long-pending relayer transactions by increasing the gas price on the transaction got stuck. Use this tool on your own risk.

**Important, read this:**

Use this tool only if you didn't have any transaction on your Matic address (hot wallet) in the last 4-6 hours otherwise you might be ruining some actual transactions being relayed.

This tool is sending the reward to the blackhole (burn) address. If you have to free up the long-pending transaction, it does not really matter, where you send the reward, since it will be rejected anyway, so no reward will be received.

Another thing you might expect. When you sent in a document to be relayed and the transaction got stuck, your relayer was definitely not aware of this and was keep relaying new and new docs. These are still in the "queue" (mempool) on the blockchain, but the pending transactions blocking them to be mined.

Therefore, **DON'T BE SURPRISED TO SEE A LOT OF DOCUMENTS TO BE FAILED ON YOUR MATIC ADDRESS** (soft wallet). This is painful, but still expected by the nature of the blockchain.

## Installation

You have to have python. Version 3.10 is recommended but the version is not a strict requirement as long as you are able install the dependencies (see below). You can check the version by running:

```sh
python -V
```

You also need `git` installed. Clone the project like this to the folder you are running the command from:

```sh
git clone https://github.com/brightknightx/cxo-free-me.git
cd cxo-free-me
```

Install the required dependencies by running:

```sh
pip3 install -r requirements.txt
```

## Usage

```sh
python3 free-me.py --private-key=12345689
```

By default 500 gwei is used as gas. This is safely enough to release the pending transactions in 99% of the cases. If you wish to change it, you can specify the desidered gas price like this (i.e. to 600 gwei):

```sh
python3 free-me.py --private-key=12345689 --gas-price=600
```
