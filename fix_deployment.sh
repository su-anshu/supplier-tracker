#!/bin/bash
# Quick fix for current deployment issues

echo "============================================================"
echo "    FIXING DEPLOYMENT ISSUES - PILLOW & STATIC FILES"
echo "============================================================"

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${GREEN}✓${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

# Install system dependencies for Pillow
print_status "Installing system dependencies for Pillow..."
sudo apt update
sudo apt install -y \
    libjpeg-dev \
    zlib1g-dev \
    libpng-dev \
    libfreetype6-dev \
    liblcms2-dev \
    libwebp-dev \
    python3-dev

# Activate virtual environment
print_status "Activating virtual environment..."
source venv/bin/activate

# Install Pillow
print_status "Installing Pillow..."
pip install Pillow==10.4.0

# Create static directory if it doesn't exist
print_status "Creating static directory..."
mkdir -p static

# Run migrations
print_status "Running database migrations..."
python manage.py migrate

# Collect static files
print_status "Collecting static files..."
python manage.py collectstatic --noinput

# Restart services
print_status "Restarting services..."
sudo systemctl restart supplier-tracker
sudo systemctl restart nginx

echo ""
echo "============================================================"
echo "               FIXES APPLIED SUCCESSFULLY!"
echo "============================================================"
echo ""
print_status "Issues fixed:"
echo "   ✓ Pillow installed for ImageField support"
echo "   ✓ Static directory created"
echo "   ✓ Database migrations completed"
echo "   ✓ Static files collected"
echo "   ✓ Services restarted"
echo ""
print_status "Your application should now be working!"
echo "   Visit: http://$(curl -s http://checkip.amazonaws.com)/"
echo ""
