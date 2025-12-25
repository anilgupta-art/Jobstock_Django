"""
Add Resume-Job Matching Navigation for RPO Admin
Creates navigation items for accessing the matching system
"""
import os
import sys
import django

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Jobstock.settings')
django.setup()

from App.models import NavigationGroup, NavigationItem
from django.urls import reverse


def main():
    print("="*80)
    print("ADDING RESUME-JOB MATCHING NAVIGATION")
    print("="*80)
    
    # Find Resume Management navigation group
    try:
        nav_group = NavigationGroup.objects.get(slug='rpo-resume-management')
        print(f"\n✓ Found Navigation Group: {nav_group.name}")
    except NavigationGroup.DoesNotExist:
        print("\n❌ Resume Management navigation group not found!")
        return
    
    # Find Dashboard parent item
    try:
        dashboard_item = NavigationItem.objects.get(
            group=nav_group,
            url_name='App:rpo_dashboard'
        )
        print(f"✓ Found Parent Item: {dashboard_item.title}")
    except NavigationItem.DoesNotExist:
        print("\n❌ Dashboard navigation item not found!")
        return
    
    # Navigation items to create
    nav_items = [
        {
            'title': 'Resume Matching',
            'url_name': 'App:resume_matching_dashboard',
            'icon': 'fa-solid fa-brain',
            'order': 4
        },
    ]
    
    # Create or update navigation items
    created_items = []
    for item_data in nav_items:
        nav_item, created = NavigationItem.objects.update_or_create(
            group=nav_group,
            title=item_data['title'],
            defaults={
                'url_name': item_data['url_name'],
                'icon': item_data['icon'],
                'parent': dashboard_item,
                'order': item_data['order'],
                'visible_to_roles': ['rpo_admin'],
                'is_active': True
            }
        )
        created_items.append((nav_item, created))
        
        action = "Created" if created else "Updated"
        print(f"\n{'✓' if created else '↻'} {action} Navigation Item:")
        print(f"   Title: {nav_item.title}")
        print(f"   URL: {nav_item.url_name}")
        print(f"   Icon: {nav_item.icon}")
        print(f"   Parent: {nav_item.parent.title if nav_item.parent else 'None'}")
        print(f"   Order: {nav_item.order}")
        print(f"   Visible to: {', '.join(nav_item.visible_to_roles)}")
    
    # Display updated navigation structure
    print(f"\n{'='*80}")
    print("UPDATED NAVIGATION STRUCTURE (RPO Admin)")
    print("="*80)
    
    print(f"\n📁 {nav_group.name}")
    
    # Get all top-level items
    top_level_items = NavigationItem.objects.filter(
        group=nav_group,
        parent__isnull=True,
        is_active=True
    ).order_by('order')
    
    for item in top_level_items:
        print(f"   ├── {item.icon} {item.title} ({item.url_name})")
        
        # Get child items
        children = NavigationItem.objects.filter(
            parent=item,
            is_active=True
        ).order_by('order')
        
        for i, child in enumerate(children):
            is_last = (i == len(children) - 1)
            prefix = "└──" if is_last else "├──"
            print(f"   │   {prefix} {child.icon} {child.title} ({child.url_name})")
    
    print(f"\n{'='*80}")
    print("✅ NAVIGATION UPDATE COMPLETE")
    print("="*80)
    
    print(f"\n📝 Features Available:")
    print(f"   ✓ Resume Matching Dashboard")
    print(f"   ✓ View all resume-job matches")
    print(f"   ✓ Match resumes to jobs")
    print(f"   ✓ View top candidates for jobs")
    print(f"   ✓ AI-powered compatibility analysis")
    
    print(f"\n🔧 Next Steps:")
    print(f"   1. Create view: App/views/matching_views.py")
    print(f"   2. Add URL route: path('resume-matching/', ...)")
    print(f"   3. Create template: templates/Pages/RPO-Admin/resume_matching_dashboard.html")
    print(f"   4. Restart Django server")
    
    print(f"\n{'='*80}")


if __name__ == "__main__":
    main()
