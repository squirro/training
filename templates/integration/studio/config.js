// For Full Documentation See: https://nektoon.atlassian.net/wiki/spaces/ENG/pages/180995718/Writing+Squirro+Studio+Plugins#WritingSquirroStudioPlugins-config.js
return StudioPlugins.Base.extend({
    index: Pages.StudioBase.extend({
        form: [
            {
                view: Properties.StaticHtml,
                config: {
                    html: '<span class="example">Hello World!</span>',
                },
            },
            {
                view: Properties.Bool,
                config: {
                    inputName: 'bool_option',
                    infoText: 'Boolean Option Example',
                    defaultValue: true
                },
            },
            {
                view: Properties.StudioButton,
                config: {
                    inputName: 'submit',
                    text: 'Submit!',
                    action: 'submit',
                },
            },
        ]
    }),
});
