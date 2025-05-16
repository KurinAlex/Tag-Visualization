# Tag Visualization

## 📖 Short overview

- Developed software is a single-page web application.
- Initial page (the one which is showed after GET request) is just a form for JSON file uploading.
- After upload (POST request) page changes layout to interactive plot with all objects and tags. From here, user have an ability to return to file upload layout using button in the top left corner.

## 💻 Launch instructions

1. Install python and pip on your system.
1. (Optional) Create and activate python virtual environment in target directory
1. Copy code to your target directory.
1. Run the following command to install required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

1. Move to `src` subdirectory.
1. Run:

    ```bash
    python manage.py runserver
    ```

1. Application will be run on localhost (usually on port 8000). Anyway, application URL will be shown in console in format:

    ```bash
    Starting development server at http://127.0.0.1:{port}/
    ```

1. Open specified application URL in your browser.

1. For running unit tests run:

    ```bash
    python manage.py test
    ```

### ❗ Important note

By default application will run in **debug** mode. If you want to switch to **production** mode, please change **DEBUG** setting value to **False** in [settings.py](src/config/settings.py) file.

In production, application will be allowed to be hosted only on **localhost**. To change this behavior, add your desired host to **ALLOWED_HOSTS** setting in [settings.py](src/config/settings.py) file.

For more information on settings, please refer to [Django documentation](http://docs.djangoproject.com/en/5.1/ref/settings/).

## ⚡ Mandatory Requirements Statuses

1. User loads JSON using web-interface. ✅
2. Application shows elements "KIT(DS)1" on 2D schema. ✅
3. For each element tag should be created, placed near: ✅
    - Must not overlap with another tag; ✅
    - Must not overlap element, which it is related to; ✅
    - Must be visually connected with object. (using color). ✅
4. Tags should be vertically or horizontally aligned. ✅

## 💡 Bonus Requirements Statuses

- Show elements of other families, highlighted with gray color. ✅
- Don't allow tag overlap with these objects. ✅

## ✨ Approach to task

First of all, draft versions of some tag placement algorithms were tested and after some experiments, **simulated annealing** algorithm showed the best results. All algorithm hyper-parameters tuning was done empirically in a series of different experiments.

Dealing with overlapping was kind of straightforward with use of high penalties. The same worked for keeping tags close to their related objects.

Among all requirements the main problem was dealing with vertical and horizontal alignment of tags, which seemed impossible due to heuristic nature of algorithm.

It was decided to randomly allow tag to align vertically or horizontally to another randomly chosen tag during step. It allowed to randomly create acceptable alignment even between distant tags on scheme.

Nevertheless, this approach can be modified to create as optimal as possible alignment between tags.

## ✅ Managed to do

- All mandatory and bonus requirements.
- Clear application architecture with respect to separation of concerns principle.
- Minimalistic web-interface for JSON uploading and tag placement results view.
- Unit tests for checking requirements compliance of implemented algorithm.
- Additional features, such as: ability to save created tag layout and interact with it thanks to `plotly` library.
- Documentation on all business logic code.

## ⏳ Planned to do if there was more time left

- Encourage tags to align with as much other tags as possible. Experiments were done, but in case of simulated annealing algorithm it leads to dramatic increase of time complexity (due to comparisons with every other tag during every computation of cost function).
- Add strategy pattern to support several tag placement algorithms, from which user can choose.
- Add validation for algorithm input hyper-parameters.
- Add more unit test coverage (for `Rectangle` class, `parse` function etc).
- Add authentication to allow users view their submission history.
- Add ability for user to control size of output scheme.
