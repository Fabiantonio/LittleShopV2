# Build script for Vercel deployment

# Make script executable
echo "Building static files..."

# Install dependencies
python3 -m pip install -r requirements.txt

# Collect static files
python3 manage.py collectstatic --noinput

# Apply migrations
python3 manage.py migrate

echo "Build completed successfully!"