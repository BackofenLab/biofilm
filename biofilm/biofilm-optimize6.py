import dirtyopts
import biofilm.util.data as datautil
import biofilm.util.out as out
import numpy as np
import structout as so
from sklearn.metrics import  f1_score
import pprint

from autosklearn.experimental.askl2 import AutoSklearn2Classifier as ASK2
from autosklearn.classification import AutoSklearnClassifier as ASK1
import autosklearn.metrics
import re 

optidoc='''
--method str any  'extra_trees', 'passive_aggressive', 'random_forest', 'sgd', 'gradient_boosting', 'mlp'
--out str jsongoeshere
--n_jobs int 1
--time int 3600
--randinit int 1337  # should be the same as the one in data.py
--preprocess bool False
#--metric str f1 assert f1 auc   TODO
'''


def get_params(ask): 
    a  =str(ask)
    classifier = re.findall("'classifier:__choice__': '(\w+)'",a)[0]
    args = re.findall(f"(classifier:{classifier}:[^,]+,)",a)
    return args
    

def optimize(X,Y,x,y, args):
    if args.method == 'any':
        estis =  ['extra_trees', 'passive_aggressive', 'random_forest', 'sgd', 'gradient_boosting', 'mlp']
    else:
        estis = [args.method]
    estim = ASK1(
            include_estimators = estis,
            include_preprocessors = ["no_preprocessing"] if not args.preprocess else None,
            n_jobs = args.n_jobs,
            ensemble_size = 1, 
            time_left_for_this_task = args.time,
            metric = autosklearn.metrics.f1,
            )
    estim.fit(X,Y)
    #import code
    #code.interact(local=dict(globals(), **locals()))
    # there is only 1 model in the end -> 0, we dont care about its weight -> 1 (this is the model) 
    #print(f" asdasdasd{estim.get_models_with_weights()}")
    estimator = estim.get_models_with_weights()[0][1] 
    return estimator, get_params(estimator)




def main():

    args = dirtyopts.parse(optidoc)
    data, fea, ins = datautil.getfold()
    estim,params = optimize(*data,args)
    out.report(estim,params, args)


    

if __name__ == "__main__":
    main()

