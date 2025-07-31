#!/bin/bash
# Quick fix for ALLOWED_HOSTS issue on EC2

echo "============================================================"
echo "    FIXING ALLOWED_HOSTS FOR AWS EC2 DEPLOYMENT"
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

# Get the public IP of this EC2 instance
PUBLIC_IP=$(curl -s http://checkip.amazonaws.com/)
INTERNAL_IP=$(hostname -I | awk '{print $1}')

print_status "Detected IPs:"
echo "   Public IP: $PUBLIC_IP"
echo "   Internal IP: $INTERNAL_IP"

# Create or update .env file
print_status "Creating/updating .env file..."

cat > .env << EOF
# Django Settings for AWS EC2
DEBUG=True
SECRET_KEY=django-insecure-aws-ec2-deployment-key-change-in-production-$(date +%s)
ALLOWED_HOSTS=localhost,127.0.0.1,$PUBLIC_IP,$INTERNAL_IP

# Company Information
COMPANY_NAME=Mithila Foods

# AWS Debug (remove after successful deployment)
AWS_DEBUG_HOSTS=False
EOF

print_status ".env file created with current EC2 IPs"

# Show the .env file contents
print_warning "Current .env configuration:"
cat .env

# Restart the application if running with systemd
if systemctl is-active --quiet supplier-tracker; then
    print_status "Restarting supplier-tracker service..."
    sudo systemctl restart supplier-tracker
    sleep 3
    sudo systemctl status supplier-tracker --no-pager
else
    print_warning "Service not running. If running manually, restart with:"
    echo "   python manage.py runserver 0.0.0.0:8000"
fi

echo ""
echo "============================================================"
echo "               ALLOWED_HOSTS FIXED!"
echo "============================================================"
echo ""
print_status "Your application should now be accessible at:"
echo "   http://$PUBLIC_IP:8000/"
echo "   http://$PUBLIC_IP:8000/admin/"
echo ""
print_warning "If still having issues, try temporarily allowing all hosts:"
echo '   echo "AWS_DEBUG_HOSTS=True" >> .env'
echo "   sudo systemctl restart supplier-tracker"
echo ""
