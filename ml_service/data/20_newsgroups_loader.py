"""
Dataloader Plugin For loading data from text files
"""
import os
import hashlib
import logging
import random
import re

from squirro.dataloader.data_source import DataSource

log = logging.getLogger(__name__)

_QUOTE_RE = re.compile(r'(writes in|writes:|wrote:|says:|said:'
                       r'|^In article|^Quoted from|^\||^>)')

class NewsgroupsSource(DataSource):
    """
    A Data loader Plugin for loading data from text files
    """

    def __init__(self):
        self.last_row = 0
        pass

    def connect(self, inc_column=None, max_inc_value=None):
        log.debug('Incremental Column: %r', inc_column)
        log.debug('Incremental Last Value: %r', max_inc_value)

    def disconnect(self):
        """Disconnect from the source."""
        pass

    def getDataBatch(self, batch_size):
        """
        Generator - Get data from source on batches.
        """
        batch_size = 1000

        directory = self.args.location
        sub_dirs = [os.path.join(directory, o) for o in os.listdir(directory)
                    if os.path.isdir(os.path.join(directory, o))]
        docs = []
        for dir in sub_dirs:
            label = dir.split('/')[-1]
            files = [os.path.join(dir, file) for file in os.listdir(dir)]
            for file in files:
                do_train = random.random() > float(self.args.validation_split)
                doc = {
                   'label': label,
                   'dataset': 'train' if do_train else 'test',
                   'body': ''
                }
                with open(file, 'rb') as f:
                    text = f.read().decode(self.args.encoding)
                    subject, text = self.strip_newsgroup_header(text)
                    text = self.strip_newsgroup_quoting(text)
                    text = self.strip_newsgroup_footer(text)
                    doc['title'] = subject
                    doc['body'] = text
                    docs.append(doc)
                    if len(docs) >= batch_size:
                        log.info('Got {} docs'.format(len(docs)))
                        yield docs
                        docs = []
        log.info('Got {} docs'.format(len(docs)))
        if docs:
            yield docs

    def getSchema(self):
        """
        Return the schema of the dataset
        :returns a List containing the names of the columns retrieved from the
        source
        """
        return [
            'id',
            'label',
            'body',
            'title'
        ]

    def getJobId(self):
        """
        Return a unique string for each different select
        :returns a string
        """
        m = hashlib.sha256()
        job_id = m.hexdigest()
        log.debug("Job ID: %s", job_id)
        return job_id

    def getArguments(self):
        """
        Get arguments required by the plugin
        """
        return [
            {
                'name': 'encoding',
                'required': True,
                'help': 'Encoding of the files to load',
            },
            {
                'name': 'location',
                'required': True,
                'help': 'Location of the files to load',
            },
            {
                'name': 'validation-split',
                'required': True,
                'help': 'Validation split between training and test datasets'
            }
        ]

    # The following taken from scikit-learn:
    # https://github.com/scikit-learn/scikit-learn/blob/a24c8b46/sklearn/datasets/twenty_newsgroups.py

    def strip_newsgroup_header(self, text):
        """
        Given text in "news" format, strip the headers, by removing everything
        before the first blank line.
        """
        _before, _blankline, after = text.partition('\n\n')
        subject = _before.split("Subject:")[-1]
        return subject, after

    def strip_newsgroup_quoting(self, text):
        """
        Given text in "news" format, strip lines beginning with the quote
        characters > or |, plus lines that often introduce a quoted section
        (for example, because they contain the string 'writes:'.)
        """
        good_lines = [line for line in text.split('\n')
                      if not _QUOTE_RE.search(line)]
        return '\n'.join(good_lines)

    def strip_newsgroup_footer(self, text):
        """
        Given text in "news" format, attempt to remove a signature block.
        As a rough heuristic, we assume that signatures are set apart by either
        a blank line or a line made of hyphens, and that it is the last such line
        in the file (disregarding blank lines at the end).
        """
        lines = text.strip().split('\n')
        for line_num in range(len(lines) - 1, -1, -1):
            line = lines[line_num]
            if line.strip().strip('-') == '':
                break

        if line_num > 0:
            return '\n'.join(lines[:line_num])
        else:
            return text
