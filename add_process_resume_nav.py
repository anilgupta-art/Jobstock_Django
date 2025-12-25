"""
Add Process Resume Navigation Item
Copies ID=45 but with custom title and URL
"""
import os
import sys
import django

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Jobstock.settings')
django.setup()

from App.models import NavigationItem


def main():
    print("="*80)
    print("ADDING PROCESS RESUME NAVIGATION")
    print("="*80)
    
    # Get the template navigation item (ID=45)
    try:
        template_item = NavigationItem.objects.get(id=45)
        print(f"\n✓ Found Template Item (ID=45):")
        print(f"   Title: {template_item.title}")
        print(f"   URL: {template_item.url_name}")
        print(f"   Icon: {template_item.icon}")
        print(f"   Group: {template_item.group.name if template_item.group else 'None'}")
        print(f"   Parent: {template_item.parent.title if template_item.parent else 'None'}")
        print(f"   Order: {template_item.order}")
        print(f"   Visible to: {', '.join(template_item.visible_to_roles)}")
    except NavigationItem.DoesNotExist:
        print("\n❌ Template navigation item (ID=45) not found!")
        return
    
    # Create new navigation item with modified title and URL
    new_item = NavigationItem.objects.create(
        group=template_item.group,
        parent=template_item.parent,
        title="Process Resume",
        url_name="App:rpo_dashboard",
        icon=template_item.icon,
        order=template_item.order + 1,  # Place it after the template item
        visible_to_roles=template_item.visible_to_roles,
        is_active=template_item.is_active
    )
    
    print(f"\n✅ Created New Navigation Item (ID={new_item.id}):")
    print(f"   Title: {new_item.title}")
    print(f"   URL: {new_item.url_name}")
    print(f"   Icon: {new_item.icon}")
    print(f"   Group: {new_item.group.name if new_item.group else 'None'}")
    print(f"   Parent: {new_item.parent.title if new_item.parent else 'None'}")
    print(f"   Order: {new_item.order}")
    print(f"   Visible to: {', '.join(new_item.visible_to_roles)}")
    
    # Display updated navigation structure
    print(f"\n{'='*80}")
    print("UPDATED NAVIGATION STRUCTURE")
    print("="*80)
    
    if new_item.group:
        print(f"\n📁 {new_item.group.name}")
        
        # Get all items in the same group
        items = NavigationItem.objects.filter(
            group=new_item.group,
            is_active=True
        ).order_by('order')
        
        # Separate parent and child items
        parent_items = items.filter(parent__isnull=True)
        
        for parent in parent_items:
            print(f"   ├── {parent.icon} {parent.title} ({parent.url_name})")
            
            # Get children
            children = items.filter(parent=parent).order_by('order')
            for i, child in enumerate(children):
                is_last = (i == len(children) - 1)
                prefix = "└──" if is_last else "├──"
                indicator = "🆕" if child.id == new_item.id else ""
                print(f"   │   {prefix} {child.icon} {child.title} ({child.url_name}) {indicator}")
    
    print(f"\n{'='*80}")
    print("✅ NAVIGATION ITEM ADDED SUCCESSFULLY")
    print("="*80)
    print(f"\nNew Item Details:")
    print(f"  • ID: {new_item.id}")
    print(f"  • Title: {new_item.title}")
    print(f"  • URL: {new_item.url_name}")
    print(f"  • Based on template ID: 45")
    print(f"\n💡 Note: The URL points to rpo_dashboard")
    print(f"   You may want to create a dedicated view for processing resumes")
    print(f"\n{'='*80}")


if __name__ == "__main__":
    main()
