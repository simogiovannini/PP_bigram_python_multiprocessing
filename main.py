import time

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


"""


int main() {
    int n_threads = 8;

    vector<long long int> seq_times, par_times;
    vector<int> ngram_lengths;

    for (int j = min_ngram_length; j <= max_ngram_length; j++) {
        ngram_lengths.push_back(j);
        cout << endl << "Length: " << j << endl;
        beg = std::chrono::high_resolution_clock::now();
        for (int p = 0; p < n_attempts; p++) {
            map<string, int> seq_ngrams = computeSequentialNgrams(corpus, j, 0, corpus.length() - 1);
        }
        end = std::chrono::high_resolution_clock::now();
        duration = std::chrono::duration_cast<std::chrono::milliseconds>(end - beg).count();
        cout << "Seq time: " << duration / n_attempts << endl;
        seq_times.push_back(duration / n_attempts);

        beg = std::chrono::high_resolution_clock::now();
        for (int p = 0; p < n_attempts; p++) {
            map<string, int> par_ngrams = computeParallelNgrams(corpus, j, n_threads);
        }
        end = std::chrono::high_resolution_clock::now();
        duration = std::chrono::duration_cast<std::chrono::milliseconds>(end - beg).count();
        cout << "Par time: " << duration / n_attempts << endl;
        par_times.push_back(duration / n_attempts);
    }

    plt::plot(ngram_lengths, seq_times);
    plt::plot(ngram_lengths, par_times);
    plt::title("Tempo di esecuzione [in millisecondi]");
    plt::save("../fig1.png");

    cout << endl;

    for(int i = 0; i < ngram_lengths.size(); i++) {
        cout << "Speedup for ngram length " << ngram_lengths[i] << ": " << (double) ((double)seq_times[i] / (double)par_times[i]) << endl;
    }

    return 0;
}


int contains(const string& str, char targetChar) {
    int index = str.find(targetChar);
    if (index != std::string::npos) return index;
    else return -1;
}

map<string, int> computeSequentialNgrams(string data, int ngram_length, int start, int end) {
    map<string, int> ngrams;
    for (int i = start; i <= end - ngram_length + 1; i++) {
        string ngram = data.substr(i, ngram_length);
        int space_index = contains(ngram, ' ');
        if(space_index != -1) {
            i += space_index;
        }
        else ngrams[ngram]++;
    }
    return ngrams;
}

map<string, int> computeParallelNgrams(string data, int ngram_length, int n_threads) {
    map<string, int> ngrams;

    int batch_size = data.length() / n_threads;

#pragma omp parallel num_threads(n_threads) default(none) shared(ngram_length, batch_size, data, ngrams)
    {
        int thread_id = omp_get_thread_num();
        int start = thread_id * batch_size;
        int end = start + batch_size - 1;

        if(thread_id == omp_get_max_threads() - 1) {
            end = data.length() - 1;
        }

        if(thread_id > 0) {
            start = start - ngram_length + 1;
        }

        map<string, int> local_ngrams;

        for (int i = start; i <= end - ngram_length + 1; i++) {
            string ngram = data.substr(i, ngram_length);
            int space_index = contains(ngram, ' ');
            if(space_index != -1) {
                i += space_index;
            }
            else local_ngrams[ngram]++;
        }

        for (auto const &pair: local_ngrams) {
        #pragma omp critical
            {
                ngrams[pair.first] += pair.second;
            }
        }

    }
    return ngrams;
}
"""