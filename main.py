import time
import multiprocessing
import math
import matplotlib.pyplot as plt


def read_input(path):
    with open(path, 'r') as file:
        corpus = file.read().replace('\n', '').lower()
    return corpus


def compute_sequential_ngrams(corpus, ngram_length):
    ngrams = {}
    i = 0
    n = len(corpus)
    while i <= n - ngram_length:
        ngram = corpus[i: i + ngram_length]
        space_index = ngram.find(' ')
        if space_index != -1:
            i += space_index
        else:
            if ngram in ngrams:
                ngrams[ngram] += 1
            else:
                ngrams[ngram] = 1
        i += 1
    return ngrams


def compute_parallel_ngrams_worker(queue, corpus, ngram_length):
    local_ngrams = compute_sequential_ngrams(corpus, ngram_length)
    queue.put(local_ngrams)
    return


def compute_parallel_ngrams(corpus, ngram_length, n_processes):
    manager = multiprocessing.Manager()
    queue = manager.Queue()
    args = []
    batch_size = math.ceil(len(corpus) / n_processes)

    for i in range(n_processes):
        start = batch_size * i
        end = min(start + batch_size, len(corpus))
        if i > 0:
            start = start - ngram_length + 1
        args.append((queue, corpus[start:end], ngram_length))

    with multiprocessing.Pool(processes=n_processes) as pool:
        pool.starmap(compute_parallel_ngrams_worker, args)

    n_grams = {}
    while not queue.empty():
        local_ngrams = queue.get()
        for k in local_ngrams.keys():
            if k not in n_grams:
                n_grams[k] = local_ngrams[k]
            else:
                n_grams[k] += local_ngrams[k]
    return n_grams


if __name__ == '__main__':
    corpus = read_input('corpus.txt')
    print(f'Corpus length: {len(corpus)}')

    min_ngram_length = 2
    max_ngram_length = 8
    n_attempts = 10
    n_threads = 8

    seq_times = []
    par_times = []

    for j in range(min_ngram_length, max_ngram_length + 1):
        print(f'Length: {j}')
        beg = time.time()
        for p in range(n_attempts):
            seq_ngrams = compute_sequential_ngrams(corpus, j)
        end = time.time()

        duration = end - beg
        print(f'Seq times: {duration / n_attempts:.5f}')
        seq_times.append(duration / n_attempts)

        beg = time.time()
        for p in range(n_attempts):
            par_ngrams = compute_parallel_ngrams(corpus, j, n_threads)
        end = time.time()

        duration = end - beg
        print(f'Par times: {duration / n_attempts:.5f}')
        par_times.append(duration / n_attempts)

    ngram_lengths = [i for i in range(min_ngram_length, max_ngram_length + 1)]
    plt.plot(ngram_lengths, seq_times, label='Sequenziale')
    plt.plot(ngram_lengths, par_times, label='Parallelizzato')
    plt.title('Tempo di esecuzione [in secondi]')
    plt.legend()
    plt.savefig('fig1.png')

    print()
    for i, len in enumerate(ngram_lengths):
        print(f'Speedup for ngram length {len}: {seq_times[i]/par_times[i]:.5f}')
