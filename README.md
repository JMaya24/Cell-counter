# Interactive ROI Selection and Cell Counter

The study of cells in neurological research is crucial for understanding their dynamic roles in brain health and disease. However, manually analyzing microscopic images can be laborious and prone to human error. To address these challenges, this project aims to develop an automated system for selecting Regions of Interest (ROIs) and counting cells, functioning similarly to a digital cell counter and ROI selector that is also interactive and user-friendly.

The project entails creating an interactive program that allows users with no prior training in image analysis to easily delineate ROIs with simple clicks, enabling automated cell counting in fluorescence images.

One drawback of using widefield microscopy, as opposed to confocal microscopy, is that widefield systems use halogen lamp illumination and filters to permit only the necessary wavelengths to pass through. This method illuminates the entire sample, resulting in a halo of light that introduces noise when trying to identify foreground objects. In contrast, confocal microscopy uses a laser system that emits only the required wavelength and benefits from having a pinhole, which focuses on a single z-region of the sample, yielding clearer images. However, a disadvantage of confocal microscopy is the longer acquisition time. For this project, since the focus was solely on cell counting, widefield microscopy and preprocessing techniques were chosen to achieve precise counts. These techniques effectively isolate areas of interest containing cells while minimizing background noise and enhancing image clarity, which aids in more accurate cell counting.


### Interactive Window Display

This window provides instructions on how to use the program.

![display_ventana](https://github.com/Maya-Arteaga/Ethanol-Cell-counter/assets/70504322/1c3d34a7-30ea-4640-9399-68defea3e889)


**Display of Images Within the Selected Directory**: Displays the images contained in the chosen directory.

**Selecting the ROI by Clicking**: Select the Region of Interest (ROI) by clicking on the area that defines it. To remove points, right-click. Once the selection is complete, press the letter "q". The selected region will then be displayed.

Once the images have been processed, this window will appear.



![ROI](https://github.com/Maya-Arteaga/Ethanol-Cell-counter/assets/70504322/fa5cb930-64bb-45d2-b356-71acac71cf3d)



**Viewing Results**: You will be able to see the results of the cell counting from the selected regions automatically in a .csv file.

![finish](https://github.com/Maya-Arteaga/Ethanol-Cell-counter/assets/70504322/24ce01d2-fea4-4475-a3ac-cf8a3df22046)

![Hippocampus_cell_counter](https://github.com/Maya-Arteaga/Ethanol-Cell-counter/assets/70504322/9131f441-cf6c-4f9f-8681-cb4249240219)

![Captura de Pantalla 2024-04-20 a la(s) 20 50 27](https://github.com/Maya-Arteaga/Ethanol-Cell-counter/assets/70504322/9293825e-842b-4d2e-8329-fc34cf9e69b5)




