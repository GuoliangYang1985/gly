import os
import gzip
import urllib.request

class DownloadMnist(object):
    @staticmethod
    def download_mnist(target_dir: str, force_redownload: bool = False) -> None:
        """
        Downloads MNIST dataset files to the specified directory.

        Args:
            target_dir: Directory to save MNIST dataset files
            force_redownload: If True, redownload files even if they exist
        """

        # Create target directory if it doesn't exist
        os.makedirs(target_dir, exist_ok=True)

        # MNIST dataset URLs (original source)
        urls = [
            'http://yann.lecun.com/exdb/mnist/train-images-idx3-ubyte.gz',
            'http://yann.lecun.com/exdb/mnist/train-labels-idx1-ubyte.gz',
            'http://yann.lecun.com/exdb/mnist/t10k-images-idx3-ubyte.gz',
            'http://yann.lecun.com/exdb/mnist/t10k-labels-idx1-ubyte.gz'
        ]

        filenames = [
            'train-images-idx3-ubyte.gz',
            'train-labels-idx1-ubyte.gz',
            't10k-images-idx3-ubyte.gz',
            't10k-labels-idx1-ubyte.gz'
        ]

        extracted_names = [
            'train-images-idx3-ubyte',
            'train-labels-idx1-ubyte',
            't10k-images-idx3-ubyte',
            't10k-labels-idx1-ubyte'
        ]

        print(f"Starting MNIST dataset download to: {target_dir}")

        # Download all compressed files
        for url, filename in zip(urls, filenames):
            filepath = os.path.join(target_dir, filename)
            extracted_path = os.path.join(target_dir, filename[:-3])  # Remove .gz extension

            # Skip if both compressed and extracted files exist and not forcing redownload
            if (os.path.exists(filepath) and os.path.exists(extracted_path)
                    and not force_redownload):
                print(f"Files already exist: {filename} and {filename[:-3]}")
                continue

            # Download the compressed file
            print(f"Downloading: {filename}")
            try:
                urllib.request.urlretrieve(url, filepath)
                print(f"Successfully downloaded: {filename}")
            except Exception as e:
                print(f"Failed to download {filename} from primary URL: {e}")
                # Try backup URL if primary fails
                print("Attempting backup URL...")
                backup_url = f'https://ossci-datasets.s3.amazonaws.com/mnist/{filename}'
                try:
                    urllib.request.urlretrieve(backup_url, filepath)
                    print(f"Successfully downloaded from backup URL: {filename}")
                except Exception as e2:
                    raise Exception(f"Cannot download {filename} from any source: {e2}")

        # Extract all downloaded files
        print("\nExtracting compressed files...")
        for filename, extracted_name in zip(filenames, extracted_names):
            gz_path = os.path.join(target_dir, filename)
            extracted_path = os.path.join(target_dir, extracted_name)

            # Skip extraction if extracted file already exists and not forcing redownload
            if os.path.exists(extracted_path) and not force_redownload:
                print(f"File already extracted: {extracted_name}")
                continue

            print(f"Extracting: {filename} -> {extracted_name}")
            try:
                with gzip.open(gz_path, 'rb') as f_in:
                    with open(extracted_path, 'wb') as f_out:
                        f_out.write(f_in.read())
                print(f"Successfully extracted: {extracted_name}")
            except Exception as e:
                print(f"Failed to extract {filename}: {e}")
                # Remove partially extracted file if exists
                if os.path.exists(extracted_path):
                    os.remove(extracted_path)
                raise

        print(f"\nMNIST dataset files have been successfully downloaded to: {target_dir}")

        # List all downloaded files
        downloaded_files = []
        for name in extracted_names + filenames:
            filepath = os.path.join(target_dir, name)
            if os.path.exists(filepath):
                file_size = os.path.getsize(filepath)
                downloaded_files.append((name, file_size))

        print("\nDownloaded files:")
        for filename, size in downloaded_files:
            print(f"  - {filename}: {size:,} bytes")

        # Calculate total size
        total_size = sum(size for _, size in downloaded_files)
        print(f"\nTotal size: {total_size:,} bytes ({total_size / (1024 * 1024):.2f} MB)")


    # Alternative simplified version using pre-processed data
    @staticmethod
    def download_mnist_simple_to_directory(target_dir: str) -> None:
        """
        Downloads MNIST dataset as a single pre-processed pickle file.

        Args:
            target_dir: Directory to save MNIST dataset files
        """

        os.makedirs(target_dir, exist_ok=True)
        filepath = os.path.join(target_dir, 'mnist.pkl.gz')

        print(f"Downloading MNIST dataset (pre-processed version) to: {target_dir}")

        # Download from reliable source
        url = 'https://github.com/mnielsen/neural-networks-and-deep-learning/raw/master/data/mnist.pkl.gz'

        try:
            urllib.request.urlretrieve(url, filepath)
            file_size = os.path.getsize(filepath)
            print(f"Successfully downloaded: mnist.pkl.gz ({file_size:,} bytes)")
            print(f"File saved to: {filepath}")
        except Exception as e:
            raise Exception(f"Failed to download MNIST dataset: {e}")