#!/bin/bash
# AWS EC2 Deployment Script for Mithila Foods Supplier Tracker

echo "============================================================"
echo "    MITHILA FOODS SUPPLIER TRACKER - AWS EC2 DEPLOYMENT"
echo "============================================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✓${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

# Check if running as root
if [ "$EUID" -eq 0 ]; then
    print_error "Please don't run this script as root"
    exit 1
fi

print_status "Starting AWS EC2 deployment..."

# Update system packages
print_status "Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install system dependencies
print_status "Installing system dependencies..."
sudo apt install -y \
    python3 \
    python3-pip \
    python3-venv \
    python3-dev \
    nginx \
    git \
    curl \
    software-properties-common \
    sqlite3

# Create application directory
APP_DIR="/home/ubuntu/supplier_tracker"
print_status "Setting up application directory: $APP_DIR"

# Create virtual environment
print_status "Creating Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
print_status "Upgrading pip..."
pip install --upgrade pip

# Install Python dependencies
print_status "Installing Python dependencies..."
pip install -r requirements.txt

# Set environment variables
print_status "Setting up environment variables..."
if [ ! -f .env ]; then
    print_warning "Creating .env file from .env.example..."
    cp .env.example .env
    print_warning "Please edit .env file with your production values"
fi

# Run database migrations
print_status "Running database migrations..."
python manage.py migrate --noinput

# Collect static files
print_status "Collecting static files..."
python manage.py collectstatic --noinput

# Create systemd service file
print_status "Creating systemd service..."
sudo tee /etc/systemd/system/supplier-tracker.service > /dev/null <<EOF
[Unit]
Description=Mithila Foods Supplier Tracker
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=$APP_DIR
Environment="PATH=$APP_DIR/venv/bin"
ExecStart=$APP_DIR/venv/bin/gunicorn --workers 3 --bind unix:$APP_DIR/supplier_tracker.sock supplier_tracker.wsgi:application
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Create Nginx configuration
print_status "Configuring Nginx..."
sudo tee /etc/nginx/sites-available/supplier-tracker > /dev/null <<EOF
server {
    listen 80;
    server_name _;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        root $APP_DIR;
    }
    
    location /media/ {
        root $APP_DIR;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:$APP_DIR/supplier_tracker.sock;
    }
}
EOF

# Enable the site
sudo ln -sf /etc/nginx/sites-available/supplier-tracker /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# Test Nginx configuration
print_status "Testing Nginx configuration..."
sudo nginx -t

# Start and enable services
print_status "Starting services..."
sudo systemctl daemon-reload
sudo systemctl start supplier-tracker
sudo systemctl enable supplier-tracker
sudo systemctl restart nginx
sudo systemctl enable nginx

# Set proper permissions
print_status "Setting file permissions..."
sudo chown -R ubuntu:www-data $APP_DIR
sudo chmod -R 755 $APP_DIR

# Show status
print_status "Checking service status..."
sudo systemctl status supplier-tracker --no-pager
sudo systemctl status nginx --no-pager

echo ""
echo "============================================================"
echo "               DEPLOYMENT COMPLETED!"
echo "============================================================"
echo ""
print_status "Your application should now be running!"
echo ""
echo "🌐 Access your application at:"
echo "   http://your-ec2-public-ip/"
echo "   http://your-ec2-public-ip/admin/"
echo ""
echo "📝 Next steps:"
echo "   1. Update your domain DNS to point to this server"
echo "   2. Set up SSL certificate with Let's Encrypt"
echo "   3. Configure backup strategy"
echo "   4. Set up monitoring"
echo ""
echo "🔧 Useful commands:"
echo "   sudo systemctl restart supplier-tracker  # Restart app"
echo "   sudo systemctl restart nginx            # Restart web server"
echo "   sudo journalctl -u supplier-tracker     # View app logs"
echo "   sudo tail -f /var/log/nginx/error.log   # View nginx logs"
echo ""
echo "⚠️  Remember to:"
echo "   - Edit .env file with production values"
echo "   - Create admin user: python manage.py createsuperuser"
echo "   - Configure firewall (Security Groups)"
echo ""
