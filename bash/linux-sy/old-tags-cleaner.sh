#!/bin/bash
output=output_file.txt  

for symlink in $(find /var/www/apps/release -type l)
do
    deployedTag=$(readlink -f $symlink)
    baseDir=$(readlink -f $deployedTag | cut -d'/' -f -5)
    appName=$(basename $baseDir)

    # echo "deployedTag $deployedTag"
    # echo "baseDir $baseDir"
    # echo "appName $appName"

    fullPath=$baseDir/*
    lscon=$(readlink -f $fullPath)
    for eachTag in $lscon
    do
        # echo "$eachTag"
        if [[ "$deployedTag" == *"$eachTag"* ]]
        then
            if [[ $eachTag == $deployedTag ]]
            then
                echo "Active => $deployedTag -> $eachTag" >> $output  
            else
                # echo "Inaccurate => $deployedTag -> $eachTag"
                subCon=$(ls -d $eachTag/*)
                for subEachTag in $subCon
                do
                    # echo "subTags $subEachTag"
                    if [[ $subEachTag == $deployedTag ]]
                    then
                        echo "Active SUB => $deployedTag -> $subEachTag" >> $output  
                    else
                        echo "Removed SUB => $subEachTag" >> $output  
                        # readlink -f $subEachTag
                    fi
                done
            fi
        else
            echo "Removed => $eachTag" >> $output
            # readlink -f $eachTag
        fi 
    done
done