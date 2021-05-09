"""
Evaluations methods common in NLP and information extraction.


TODO: Have a look at
  https://github.com/nschneid/pyutil/blob/master/chunkeval.py, there appear to be
  richer evaluation methods.

"""


from collections import defaultdict


class F1:

    def __init__(self, confusion_matrix=False):
        if confusion_matrix:
            self.confusion_matrix = defaultdict(lambda : defaultdict(int))
        else:
            self.confusion_matrix = None
        self.n_examples = 0
        self.relevant  = defaultdict(set)
        self.retrieved = defaultdict(set)

    def report(self, instance, prediction, target):
        if self.confusion_matrix is not None:
            self.confusion_matrix[target][prediction] += 1
        self.n_examples += 1
        self.add_relevant(target, instance)
        self.add_retrieved(prediction, instance)

    def add_relevant(self, label, instance):
        self.relevant[label].add(instance)

    def add_retrieved(self, label, instance):
        self.retrieved[label].add(instance)
        return instance in self.relevant[label]

    def latex(self):
        relevant  = self.relevant
        retrieved = self.retrieved

        print(r"""
\begin{tabular}{|l|c|c|c|c|}
\hline
 Label         &   Count   &   Precision   &   Recall   &   $F_1$   \\
\hline""")

        tbl = []
        labels = list(self.relevant.keys())
        labels.sort()
        for label in labels:
            R = P = F = 0
            count = len(relevant[label])
            top = relevant[label] & retrieved[label]
            if len(relevant[label]) != 0:
                R = len(top) / len(relevant[label])
            if len(retrieved[label]) != 0:
                P = len(top) / len(retrieved[label])
            if P + R != 0:
                F = 2*P*R / (P + R)
            print(r' %8s & %5d & %5.1f & %5.1f & %5.1f \\' % (label, count, P*100, R*100, F*100))
            tbl.append((label,count,P,R,F))

        print(r"""\hline
\end{tabular}
""")
        return tbl

    def scores(self, verbose=True):
        relevant  = self.relevant
        retrieved = self.retrieved
        if verbose:
            m = max(list(map(len, self.relevant))) if self.relevant else 0
            fmt = ' | %{0}s | %5d | %5.1f | %5.1f | %5.1f |'.format(m)

            line = ' |' + '='*m + '==================================|'

            print(line)
            print(' |', ' '*m, '|   C   |   P   |   R   |   F   |')
            print(line)

        tbl = []
        labels = list(self.relevant.keys())
        labels.sort()
        for label in labels:
            R = P = F = 0
            count = len(relevant[label])
            top = relevant[label] & retrieved[label]
            if len(relevant[label]) != 0:
                R = len(top) / len(relevant[label])
            if len(retrieved[label]) != 0:
                P = len(top) / len(retrieved[label])
            if P + R != 0:
                F = 2*P*R / (P + R)
            if verbose:
                print(fmt % (label, count, P*100, R*100, F*100))
                #t.add_row([label, P*100, R*100, F*100])
            tbl.append((label,count,P,R,F))
        if verbose:
            print(line)
            #print t
        return tbl

    def confusion(self):
        assert self.confusion_matrix is not None
        for t, predictions in self.confusion_matrix.items():
            incorrect = sum(cnt for p,cnt in list(predictions.items()) if t != p)
            print('%s [correct: %s; incorrect: %s]' % (t, predictions[t], incorrect))
            for predicted, cnt in predictions.items():
                if t != predicted:
                    incorrect += cnt
                    print('      %6s -> %s' % (predicted, cnt))
            print()


def plot_confusion(y_true, y_pred, alphabet, normalized=False):
    """
    Draw confusion matrix

    Options:

     - normalized: Normalize the confusion matrix by row (i.e by the number of samples in each
       class)

    """
    import numpy as np
    import matplotlib.pyplot as pl

    from sklearn.metrics import confusion_matrix

    def plot_confusion_matrix(cm, title='Confusion matrix', cmap=pl.cm.Blues):
        pl.imshow(cm, interpolation='nearest', cmap=cmap)
        pl.title(title)
        pl.colorbar()
        target_names = list(alphabet)
        tick_marks = np.arange(len(target_names))
        pl.xticks(tick_marks, target_names, rotation=45)
        pl.yticks(tick_marks, target_names)
        pl.tight_layout()
        pl.ylabel('True label')
        pl.xlabel('Predicted label')

    # Compute confusion matrix
    cm = confusion_matrix(y_true, y_pred)
    np.set_printoptions(precision=2)

    if normalized:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]

    print(cm)

    pl.figure()
    plot_confusion_matrix(cm, title='Confusion matrix')

    pl.show()
