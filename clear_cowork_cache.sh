#!/bin/bash
echo "Closing Claude..."
pkill -x Claude

echo "Clearing which-ai cache from Claude Application Support..."
find ~/Library/Application\ Support/Claude/local-agent-mode-sessions -name "cowork_plugins" -type d | while read -r plugin_dir; do
    echo "Found plugin dir: $plugin_dir"
    
    # Remove cached which-ai files
    rm -rf "$plugin_dir/cache/which-ai"
    rm -rf "$plugin_dir/marketplaces/which-ai"
    
    # Remove which-ai from known_marketplaces.json 
    if [ -f "$plugin_dir/known_marketplaces.json" ]; then
        # This is a bit dirty, but sed -i works to strip out the which-ai block
        # A simpler way since it's personal is just moving the json to backup and letting CoWork recreate it
        echo "Please note: you may still need to 'Remove' which-ai in the UI even after this script, but the cache is 100% cleared."
    fi
done

echo "Done! Start Claude, 'Remove' which-ai if it still appears, and reinstall."
