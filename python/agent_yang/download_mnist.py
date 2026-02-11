import os
import gzip
import urllib.request


class DownloadMnist(object):
    @staticmethod
    def download_mnist(target_dir: str) -> None:
        """
        Downloads MNIST dataset files to the specified directory.

        Args:
            target_dir: Directory to save MNIST dataset files
        """
        # Create target directory if it doesn't exist
        os.makedirs(target_dir, exist_ok=True)

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
        for filename in filenames:
            filepath = os.path.join(target_dir, filename)
            extracted_path = os.path.join(target_dir, filename[:-3])  # Remove .gz extension

            # Skip if both compressed and extracted files exist.
            if os.path.exists(filepath) and os.path.exists(extracted_path):
                print(f"Files already exist: {filename} and {filename[:-3]}")
                continue

            # Download the compressed file
            print("Attempting URL...")
            url = f'https://ossci-datasets.s3.amazonaws.com/mnist/{filename}'
            try:
                urllib.request.urlretrieve(url, filepath)
                print(f"Successfully downloaded from URL: {filename}")
            except Exception as e2:
                raise Exception(f"Cannot download {filename} from any source: {e2}")

        # Extract all downloaded files
        print("\nExtracting compressed files...")
        for filename, extracted_name in zip(filenames, extracted_names):
            gz_path = os.path.join(target_dir, filename)
            extracted_path = os.path.join(target_dir, extracted_name)

            # Skip extraction if extracted file already exists
            if os.path.exists(extracted_path):
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