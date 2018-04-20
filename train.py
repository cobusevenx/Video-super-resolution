import argparse
import sys
import os
from SR_datasets import DatasetFactory
from model import ModelFactory
from solver import Solver
from loss import get_loss_fn
description='Video Super Resolution pytorch implementation'

parser = argparse.ArgumentParser(description=description)

parser.add_argument('-m', '--model', metavar='M', type=str, default='VRES',
                    help='network architecture. Default VRES')
parser.add_argument('-s', '--scale', metavar='S', type=int, default=3, 
                    help='interpolation scale. Default 3')
parser.add_argument('--train-set', metavar='T', type=str, default='train',
                    help='data set for training. Default train')
parser.add_argument('-b', '--batch-size', metavar='B', type=int, default=100,
                    help='batch size used for training. Default 100')
parser.add_argument('-l', '--learning-rate', metavar='L', type=float, default=1e-3,
                    help='learning rate used for training. Default 1e-3')
parser.add_argument('-n', '--num-epochs', metavar='N', type=int, default=50,
                    help='number of training epochs. Default 100')
parser.add_argument('-f', '--fine-tune', dest='fine_tune', action='store_true',
                    help='fine tune the model under check_point dir,\
                    instead of training from scratch. Default False')
parser.add_argument('-v', '--verbose', dest='verbose', action='store_true',
                    help='print training information. Default False')

args = parser.parse_args()

def get_full_path(scale, train_set):

    scale_path = str(scale) + 'x'
    return os.path.join('preprocessed_data', train_set, scale_path)
    



def main():
    display_config()

    dataset_root = get_full_path(args.scale, args.train_set)

    print('Constructing dataset...')
    dataset_factory = DatasetFactory()
    train_dataset  = dataset_factory.create_dataset(args.model,
                                                    dataset_root)

    model_factory = ModelFactory()
    model = model_factory.create_model(args.model)
    
    loss_fn = get_loss_fn(model.name)

    check_point = os.path.join('check_point', model.name, str(args.scale) + 'x')

    solver = Solver(model, check_point, loss_fn=loss_fn, batch_size=args.batch_size,
                    num_epochs=args.num_epochs, learning_rate=args.learning_rate,
                    fine_tune=args.fine_tune, verbose=args.verbose)

    print('Training...')
    solver.train(train_dataset)
if __name__ == '__main__':
    main()

